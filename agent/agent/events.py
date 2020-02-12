import socketio
from devices import hwalert
from models import Device
from utils.general import reload_config
from config import config

# sio = socketio.Client()
# sio.connect(config.WS_HOST, namespaces=['/alert', '/device'])

# @sio.on('serverMsg', namespace='/alert')
# def on_message(msg):
#     if msg == 'stop_alert':
#         print('Alert stopped')
#         hwalert.stop_alert()

# @sio.on('update_device', namespace='/device')
# def update_device(msg):
#     device = reload_config()
#     if device.alarm:
#         hwalert.on('Web Triggered')
#     else:
#         hwalert.stop_alert()
