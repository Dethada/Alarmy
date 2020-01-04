import threading
from db import session
from config import config
from models import Device
from nanpy import ArduinoApi, SerialManager

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


def nanpy_connect():
    connection = SerialManager()
    arduinoObject = ArduinoApi(connection=connection)
    return arduinoObject


def reload_config():
    device = session.query(Device).first()
    config.POLL_INTERVAL = device.poll_interval
    config.POLL_INTERVAL = device.poll_interval
    config.ALARM_DURATION = device.alarm_duration
    config.ALERT_INTERVAL = device.alert_interval
    config.FROM_ADDR = device.email
    config.VFLIP = device.vflip
    config.MOTD = device.motd
    config.KEYPAD_CODE = device.alarm_code
    config.DETECT_HUMANS = device.detect_humans
    return device
