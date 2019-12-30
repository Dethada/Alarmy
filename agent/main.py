#!/usr/bin/env python3
import os
import json
from time import sleep
from datetime import datetime
from base64 import b64encode
from typing import Optional
import threading
from gpiozero import MotionSensor
import numpy as np
import cv2
from gpiozero import DigitalInputDevice
from utils import nanpy_connect, Thread, HWAlert, publish_single
from mq2 import MQ2
import db
import models
from dotenv import load_dotenv
load_dotenv()


ALARM_DURATION = int(os.getenv('ALARM_DURATION'))
POLL_INTERVAL = int(os.getenv('POLL_INTERVAL'))
ALERT_INTERVAL = int(os.getenv('ALERT_INTERVAL'))
LM35_PIN = os.getenv('LM35_PIN')
BUZZER_PIN = os.getenv('BUZZER_PIN')
MOTION_PIN = os.getenv('MOTION_PIN')
VFLIP = True

mq = MQ2()
arduino = nanpy_connect()
arduino.pinMode(LM35_PIN, arduino.INPUT)
lock = threading.Lock()
hwalert = HWAlert(BUZZER_PIN)


def insert_current_data():
    perc = mq.MQPercentage()
    gas = models.Gas(lpg=perc['GAS_LPG'], co=perc['CO'], smoke=perc['SMOKE'])
    temp_c = (arduino.analogRead(LM35_PIN) * 500) / 1024
    print('Temp: {0:.2f} C'.format(temp_c))
    temp = models.Temperature(value=temp_c)
    print(gas)
    with lock:
        db.session.add(gas)
        db.session.add(temp)
        db.session.commit()


def insert_alert_data(reason):
    perc = mq.MQPercentage()
    current_time = datetime.now()
    gas = models.Gas(lpg=perc['GAS_LPG'], co=perc['CO'],
                     smoke=perc['SMOKE'], capture_time=current_time)
    temp_c = (arduino.analogRead(LM35_PIN) * 500) / 1024
    print('Temp: {0:.2f} C'.format(temp_c))
    temp = models.Temperature(value=temp_c, capture_time=current_time)
    print(gas)
    with lock:
        db.session.add(gas)
        db.session.add(temp)
        db.session.commit()
    gas_ticker = db.session.query(models.Gas).filter(
        models.Gas.capture_time == current_time).first().ticker
    temp_ticker = db.session.query(models.Temperature).filter(
        models.Temperature.capture_time == current_time).first().ticker
    envalert = models.EnvAlert(
        reason=reason, gas_ticker=gas_ticker, temp_ticker=temp_ticker, alert_time=current_time)
    with lock:
        db.session.add(envalert)
        db.session.commit()
    return {'time': current_time, 'gas': gas, 'temp': temp}


def watch_gas_alerts():
    dpin = DigitalInputDevice(26, pull_up=True)

    while True:
        dpin.wait_for_active()
        print('Alert')
        reason = 'Gases Detected'
        info = insert_alert_data(reason)
        msg = {'subject': 'Gases Detected',
               'content': f'Time: {info["time"]}<br>Temp: {round(info["temp"].value, 2)} LPG: {round(info["gas"].lpg, 5)} CO: {round(info["gas"].co, 5)} Smoke: {round(info["gas"].smoke, 5)}'}
        publish_single('/alert', json.dumps(msg))
        hwalert.run_for(reason, ALARM_DURATION)
        sleep(ALERT_INTERVAL)


def poll_env_data():
    while True:
        insert_current_data()
        sleep(POLL_INTERVAL)


# hwalert = HWAlert(BUZZER_PIN)
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# open webcam video stream
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


def detect_person_frame(src_frame: np.ndarray) -> Optional[np.ndarray]:
    """Detect if a person is in a frame.

    Args:
        src_frame (ndarray): The first parameter.

    Returns:
        (ndarray, optional): The return value. True for success, False otherwise.

    """
    # resizing for faster detection
    frame = cv2.resize(src_frame, (640, 480))
    # using a greyscale picture, also for faster detection
    # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    if boxes.any():
        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)

        return frame
    return None


def insert_data(img_data):
    current_time = datetime.now()
    person_alert = models.PersonAlert(image=img_data, alert_time=current_time)
    db.session.add(person_alert)
    db.session.commit()
    return current_time


def detect_person():
    _, frame = cap.read()
    if VFLIP:
        frame = cv2.flip(frame, 0)
    res = detect_person_frame(frame)
    if res is not None:
        print('Person detected')
        # sound buzzer & save frame to img & send notification
        _, buffer_img = cv2.imencode('.jpg', res)
        img_data = f'{b64encode(buffer_img).decode()}'
        alert_time = insert_data(img_data)
        print('Person detected')
        publish_single('/alert', json.dumps(
            {'subject': 'Person detected', 'content': f'Person detected at {alert_time}<br><img src="cid:defaultcid"/>', 'img_attachment': img_data}))
        hwalert.run_for('Person Detected', ALARM_DURATION)
        sleep(ALERT_INTERVAL)
    else:
        cv2.imwrite("dumps/nope.jpg", frame)
        print('False alarm')


def detect_humans():
    pir = MotionSensor(MOTION_PIN, sample_rate=5, queue_len=1)
    print('Started...')

    pir.when_motion = detect_person

    while True:
        pass

def main():
    gas_alerts_thread = Thread(watch_gas_alerts)
    poll_env_thread = Thread(poll_env_data)
    human_thread = Thread(detect_humans)


if __name__ == "__main__":
    main()