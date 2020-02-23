import json
import base64
from config import config
from devices import hwalert
from utils import write_config

immutable_configs = {'DEVICE_ID'}

def update_config(payload):
    d = json.loads(payload)
    alarm_msg = ''
    for key, value in d.items():
        if key in config and key not in immutable_configs and not key.endswith('PIN'):
            if key == 'ALARM_ON':
                if value == True:
                    hwalert.on(alarm_msg)
                else:
                    print('Alert stopped')
                    hwalert.stop_alert()
            elif key == 'ALARM_MSG':
                alarm_msg = value
            config[key] = value
    write_config()


def message_handler(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = base64.b64decode(message.payload.decode('utf-8')).decode('utf-8')
    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))
    if message.topic == config['TMP']['CONFIG_TOPIC']:
        update_config(payload)
