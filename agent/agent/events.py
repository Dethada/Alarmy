import json
from config import config
from utils import general

immutable_configs = {'DEVICE_ID'}

def update_config(payload):
    d = json.loads(payload)
    for key, value in d.items():
        if key in config and key not in immutable_configs and not key.endswith('PIN'):
            config[key] = value
    general.write_config()


def message_handler(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload.decode('utf-8'))
    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))
    if message.topic == config['CONFIG_TOPIC']:
        update_config(payload)
