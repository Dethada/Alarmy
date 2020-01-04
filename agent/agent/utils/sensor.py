from db import session
from models import Device
from .notifyer import broadcast_mail
from events import sio

def ws_notify_users(msg):
    sio.emit('alert_users', msg, namespace='/alert')

def new_values():
    sio.emit('new_values', '', namespace='/alert')


def trigger_alert_helper(msg):
    ws_notify_users(msg)
    new_values()
    device = session.query(Device).first()
    device.alarm = True
    session.commit()


def trigger_env_alert(reason, time, temp, lpg, co, smoke):
    mail = {'subject': reason,
        'content': f'Time: {time}<br>Temp: {round(temp, 2)} LPG: {round(lpg, 5)} CO: {round(co, 5)} Smoke: {round(smoke, 5)}'}
    broadcast_mail(mail)
    trigger_alert_helper(reason)
