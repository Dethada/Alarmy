import json
import copy
import threading
from datetime import datetime
from comms import mqttc
from config import config

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


def reload_config():
    with open('config.json') as json_file:
        config = json.load(json_file)
        config['DEVICE_TOPIC'] = f'devices/{config["DEVICE_ID"]}/'
        config['CONFIG_TOPIC'] = f'{config["DEVICE_TOPIC"]}config'
        config['ALERT_TOPIC'] = f'{config["DEVICE_TOPIC"]}alert'
    return config

def write_config():
    tmp_config = copy.deepcopy(config)
    tmp_config.pop('DEVICE_TOPIC', None)
    tmp_config.pop('CONFIG_TOPIC', None)
    tmp_config.pop('ALERT_TOPIC', None)
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(tmp_config, f, ensure_ascii=False, indent=2)

def publish(topic, data):
    mqttc.publish(f"{config['DEVICE_TOPIC']}{topic}", json.dumps(data))

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
