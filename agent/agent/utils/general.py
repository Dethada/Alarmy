import json
import threading
from datetime import datetime
from db import session
from comms import mqttc
from config import config
from models import Device

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


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
    config.TEMP_THRESHOLD = device.temp_threshold
    return device

def publish(topic, data):
    mqttc.publish(f"devices/{config.DEVICE_ID}/{topic}", json.dumps(data))

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
