import json
import threading
from datetime import datetime
from comms import mqttc
from config import config

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


def reload_config():
    '''
    {
        'BUZZER_PIN': 21,
        'MQ2_APIN': 0,
        'MQ2_DPIN': 26,
        'LM35_PIN': 1,
        'MOTION_PIN': 13,
        'ALARM_DURATION': 60,
        'POLL_INTERVAL': 60,
        'ALERT_INTERVAL': 60,
        'TEMP_THRESHOLD': 50,
        'KEYPAD_CODE': '1234',
        'MOTD': 'MOTD',
        'VFLIP': False,
        'DETECT_HUMANS': False,
    }
    '''
    with open('config.json') as json_file:
        config = json.load(json_file)
        return config

def write_config():
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def publish(topic, data):
    mqttc.publish(f"devices/{config.DEVICE_ID}/{topic}", json.dumps(data))

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
