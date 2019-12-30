#!/usr/bin/env python3
import os
import json
from time import sleep
from datetime import datetime
from base64 import b64encode
from typing import Optional
from gpiozero import Buzzer
from gpiozero import MotionSensor
import numpy as np
import cv2
import db
from models import PersonAlert
from utils import publish_single, Thread
from dotenv import load_dotenv
load_dotenv()

MOTION_PIN = os.getenv('MOTION_PIN')
BUZZER_PIN = os.getenv('BUZZER_PIN')
VFLIP = True

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
    person_alert = PersonAlert(image=img_data, alert_time=current_time)
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
        # cv2.imwrite("dumps/detected.jpg", res)
        sleep(60)
    else:
        cv2.imwrite("dumps/nope.jpg", frame)
        print('False alarm')


def test():
    pir = MotionSensor(MOTION_PIN, sample_rate=5, queue_len=1)
    print('Started...')

    pir.when_motion = detect_person

    while True:
        pass

def main():
    t1 = Thread(test)

if __name__ == "__main__":
    main()
