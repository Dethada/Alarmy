#!/usr/bin/env python3
from time import sleep
from datetime import datetime
import threading
from gpiozero import DigitalInputDevice
from utils import Thread, reload_config
from notifyer import broadcast_mail
from events import ws_notify_users, new_values
from detection import detect_person_frame, detect_humans
import db
import models
from config import config
from devices import arduino, mq, keylock, hwalert, mq2_alert


lock = threading.Lock()


def get_temp():
    return (arduino.analogRead(config.LM35_PIN) * 500) / 1024


def get_gases():
    perc = mq.MQPercentage()
    return models.Gas(lpg=perc['GAS_LPG'], co=perc['CO'], smoke=perc['SMOKE'])


def store_env_data(gas, temp):
    with lock:
        db.session.add(gas)
        db.session.add(temp)
        db.session.commit()


def insert_current_data():
    gas = get_gases()
    temp_c = get_temp()
    temp = models.Temperature(value=temp_c)
    print('Temp: {0:.2f} C'.format(temp_c))
    print(gas)
    store_env_data(gas, temp)


def insert_alert_data(reason):
    current_time = datetime.now()
    gas = get_gases()
    gas.capture_time = current_time
    temp_c = get_temp()
    temp = models.Temperature(value=temp_c, capture_time=current_time)
    print('Temp: {0:.2f} C'.format(temp_c))
    print(gas)
    store_env_data(gas, temp)
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
    while True:
        mq2_alert.wait_for_active()
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
    device = reload_config()
    if device.alarm:
        hwalert.on('')
    gas_alerts_thread = Thread(watch_gas_alerts)
    poll_env_thread = Thread(poll_env_data)
    human_thread = Thread(detect_humans)
    keylock.start()


if __name__ == "__main__":
    main()
