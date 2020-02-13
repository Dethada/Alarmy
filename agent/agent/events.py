import json
from config import config
from devices import hwalert
from utils import write_config

immutable_configs = {'DEVICE_ID'}

def update_config(payload):
    d = json.loads(payload)
    for key, value in d.items():
        if key in config and key not in immutable_configs and not key.endswith('PIN'):
            if key == 'ALARM_ON' and value['on'] != config[key]:
                if value['on']:
                    hwalert.on(value['reason'])
                else:
                    print('Alert stopped')
                    hwalert.stop_alert()
            config[key] = value
    write_config()


def message_handler(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload.decode('utf-8'))
    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))
    if message.topic == config['TMP']['CONFIG_TOPIC']:
        update_config(payload)
