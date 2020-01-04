import sys
import time
import adafruit_matrixkeypad
from digitalio import DigitalInOut
import board
from hwalert import hwalert
from models import Device
from config import config
from db import session


class KeyLock():
    def __init__(self, hwalert, config):
        self.config = config
        self.code = ''
        self.hwalert = hwalert
        self.armed = False

    def enter_key(self, key):
        if not self.armed:
            device = session.query(Device).first()
            self.armed = device.alarm
        if self.armed:
            self.code = self.code + key
            length = len(self.code)
            self.hwalert.lcd.text('*' * length, 2)

    def clear(self):
        self.code = ''
        self.hwalert.lcd.text(self.hwalert.msg, 2)

    def disarm(self):
        self.hwalert.stop_alert()
        self.armed = False

    def authenticate(self):
        if self.config.KEYPAD_CODE == self.code:
            self.disarm()
            device = session.query(Device).first()
            device.alarm = False
            session.commit()
        else:
            self.hwalert.lcd.text('Incorrect!', 2)
            time.sleep(1)
            self.clear()


# 4x4 matrix keypad
rows = [DigitalInOut(x) for x in (board.D4, board.D17, board.D27, board.D22)]
cols = [DigitalInOut(x) for x in (board.D18, board.D23, board.D24, board.D25)]
keys = (('1', '2', '3', 'A'),
        ('4', '5', '6', 'B'),
        ('7', '8', '9', 'C'),
        ('*', '0', '#', 'D'))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

# set passcode here
keylock = KeyLock(hwalert, config)


def check_keypad_input():
    while True:
        keys = keypad.pressed_keys
        if keys:
            if keys[0] == 'C':
                keylock.clear()
            elif keys[0] == '*':
                keylock.authenticate()
            else:
                keylock.enter_key(keys[0])
            time.sleep(0.2)
