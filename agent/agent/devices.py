from gpiozero import MotionSensor, Buzzer, DigitalInputDevice
from rpi_lcd import LCD
from utils import nanpy_connect
from mq2 import MQ2
from hwalert import HWAlert
from keypad import KeyLock
from config import config

arduino = nanpy_connect()
arduino.pinMode(config.LM35_PIN, arduino.INPUT)

mq = MQ2(config.MQ2_PIN, arduino)
lcd = LCD()
buzzer = Buzzer(config.BUZZER_PIN)

hwalert = HWAlert(lcd, buzzer)

keylock = KeyLock(hwalert, lcd)

pir = MotionSensor(config.MOTION_PIN, sample_rate = 5, queue_len = 1)

mq2_alert = DigitalInputDevice(26, pull_up=True)