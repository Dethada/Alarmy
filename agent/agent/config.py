import json

with open('config.json') as json_file:
    config = json.load(json_file)
    config['TMP'] = dict()
    config['TMP']['DEVICE_TOPIC'] = f'devices/{config["DEVICE_ID"]}/'
    config['TMP']['CONFIG_TOPIC'] = f'{config["TMP"]["DEVICE_TOPIC"]}config'
    config['TMP']['ALERT_TOPIC'] = f'{config["TMP"]["DEVICE_TOPIC"]}alert'
