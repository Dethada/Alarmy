import socketio
from devices import hwalert
from db import session
from models import Device
from utils import reload_config
from config import config

sio = socketio.Client()
sio.connect('http://localhost:5000', namespaces=['/alert', '/device'])

@sio.on('serverMsg', namespace='/alert')
def on_message(msg):
    if msg == 'stop_alert':
        print('Alert stopped')
        hwalert.stop_alert()

@sio.on('update_device', namespace='/device')
def update_device(msg):
    device = reload_config()
    if device.alarm:
        hwalert.on('Web Triggered')
    else:
        hwalert.stop_alert()

def ws_notify_users(msg):
    sio.emit('alert_users', msg, namespace='/alert')

def new_values():
    sio.emit('new_values', '', namespace='/alert')