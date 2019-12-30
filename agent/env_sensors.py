#!/usr/bin/env python3
import os
import json
from time import sleep
from datetime import datetime
import threading
from gpiozero import DigitalInputDevice
import paho.mqtt.publish as publish
from utils import nanpy_connect, Thread, HWAlert
from mq2 import MQ2
import db
import models
from dotenv import load_dotenv
load_dotenv()


POLL_INTERVAL = int(os.getenv('POLL_INTERVAL'))
ALERT_INTERVAL = int(os.getenv('ALERT_INTERVAL'))
LM35_PIN = os.getenv('LM35_PIN')
BUZZER_PIN = os.getenv('BUZZER_PIN')

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


def alert_thread():
    dpin = DigitalInputDevice(26, pull_up=True)

    while True:
        hwalert.off()
        dpin.wait_for_active()
        print('Alert')
        reason = 'Gases Detected'
        info = insert_alert_data(reason)
        msg = {'subject': 'Gases Detected',
               'content': f'Time: {info["time"]}<br>Temp: {round(info["temp"].value, 2)} LPG: {round(info["gas"].lpg, 5)} CO: {round(info["gas"].co, 5)} Smoke: {round(info["gas"].smoke, 5)}'}
        publish.single("/alert", json.dumps(msg), hostname="192.168.1.17")
        hwalert.on(reason)
        sleep(ALERT_INTERVAL)


def poll_thread():
    while True:
        insert_current_data()
        sleep(POLL_INTERVAL)


def main():
    t1 = Thread(alert_thread)
    t2 = Thread(poll_thread)


if __name__ == "__main__":
    main()
