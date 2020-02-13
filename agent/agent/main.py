#!/usr/bin/env python3
from time import sleep
from datetime import datetime
import threading
from utils import Thread, reload_config, get_current_time
from comms import publish
from devices.detection import detect_humans
from config import config
from devices import arduino, mq, keylock, hwalert, mq2_alert, lcd


lock = threading.Lock()


def get_temp():
    return (arduino.analogRead(config['LM35_PIN']) * 500) / 1024


def get_gases():
    perc = mq.MQPercentage()
    return {'lpg':perc['GAS_LPG'], 'co':perc['CO'], 'smoke': perc['SMOKE']}


def store_env_data(gas, temp):
    with lock:
        publish('data', {'time': get_current_time(), 'gas': gas, 'temp': temp})


def insert_current_data():
    gas = get_gases()
    temp_c = get_temp()
    print('Temp: {0:.2f} C'.format(temp_c))
    # print(gas)
    store_env_data(gas, temp_c)


def poll_env_data():
    while True:
        insert_current_data()
        sleep(config['POLL_INTERVAL'])


def insert_alert_data(type):
    current_time = get_current_time()
    gas = get_gases()
    temp_c = get_temp()
    print('Temp: {0:.2f} C'.format(temp_c))
    print(gas)
    data = {'time': current_time, 'gas': gas, 'temp': temp_c}
    with lock:
        publish(f'alerts/{type}', data)
    return data


def watch_gas_alerts():
    while True:
        mq2_alert.wait_for_active()
        reason = 'Gases Detected'
        info = insert_alert_data('gas')
        hwalert.run_for(reason, config['ALARM_DURATION'])
        sleep(config['ALERT_INTERVAL'])


def watch_temp():
    while True:
        temp = get_temp()
        if temp > config['TEMP_THRESHOLD']:
            reason = 'High Temperature'
            info = insert_alert_data('temp')
            hwalert.run_for(reason, config['ALARM_DURATION'])
            sleep(config['ALERT_INTERVAL'])
        sleep(1)


def main():
    if config['ALARM_ON']:
        hwalert.on('')
    else:
        lcd.text(config['MOTD'], 1)
    gas_alerts_thread = Thread(watch_gas_alerts)
    poll_env_thread = Thread(poll_env_data)
    human_thread = Thread(detect_humans)
    temp_thread = Thread(watch_temp)
    keylock.start()


if __name__ == "__main__":
    main()
