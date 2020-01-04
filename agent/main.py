#!/usr/bin/env python3
from time import sleep
from datetime import datetime
from base64 import b64encode
from typing import Optional
import threading
from gpiozero import MotionSensor
import numpy as np
import cv2
from gpiozero import DigitalInputDevice
from utils import nanpy_connect, Thread
from hwalert import hwalert
from notifyer import broadcast_mail
from mq2 import mq
from events import sio, ws_notify_users, new_values
from detection import detect_person_frame, detect_humans
import db
import models
from config import config
from keypad import check_keypad_input

arduino = nanpy_connect()
arduino.pinMode(config.LM35_PIN, arduino.INPUT)
lock = threading.Lock()


def insert_current_data():
    perc = mq.MQPercentage()
    gas = models.Gas(lpg=perc['GAS_LPG'], co=perc['CO'], smoke=perc['SMOKE'])
    temp_c = (arduino.analogRead(config.LM35_PIN) * 500) / 1024
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
    temp_c = (arduino.analogRead(config.LM35_PIN) * 500) / 1024
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
        ws_notify_users('Gases Detected')
        broadcast_mail(msg)
        device = db.session.query(models.Device).first()
        device.alarm = True
        db.session.commit()
        hwalert.run_for(reason, config.ALARM_DURATION)
        sleep(config.ALERT_INTERVAL)


def poll_env_data():
    while True:
        insert_current_data()
        new_values()
        sleep(config.POLL_INTERVAL)


def main():
    device = db.session.query(models.Device).first()
    config.POLL_INTERVAL = device.poll_interval
    config.ALARM_DURATION = device.alarm_duration
    config.ALERT_INTERVAL = device.alert_interval
    config.FROM_ADDR = device.email
    config.VFLIP = device.vflip
    config.MOTD = device.motd
    config.KEYPAD_CODE = device.alarm_code
    if device.alarm:
        hwalert.on('')
    gas_alerts_thread = Thread(watch_gas_alerts)
    poll_env_thread = Thread(poll_env_data)
    human_thread = Thread(detect_humans)
    keypad_thread = Thread(check_keypad_input)


if __name__ == "__main__":
    main()
