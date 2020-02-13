import json

with open('config.json') as json_file:
    config = json.load(json_file)
    config['DEVICE_TOPIC'] = f'devices/{config["DEVICE_ID"]}/'
    config['CONFIG_TOPIC'] = f'{config["DEVICE_TOPIC"]}config'
    config['ALERT_TOPIC'] = f'{config["DEVICE_TOPIC"]}alert'
