from picamera import PiCamera
from gpiozero import MotionSensor, Buzzer, DigitalInputDevice
from nanpy import ArduinoApi, SerialManager
from rpi_lcd import LCD
from .mq2 import MQ2
from .hwalert import HWAlert
from .keypad import KeyLock
from config import config

def nanpy_connect():
    connection = SerialManager()
    arduinoObject = ArduinoApi(connection=connection)
    return arduinoObject

arduino = nanpy_connect()
arduino.pinMode(config['LM35_PIN'], arduino.INPUT)

mq = MQ2(config['MQ2_APIN'], arduino)
lcd = LCD()
buzzer = Buzzer(config['BUZZER_PIN'])

hwalert = HWAlert(lcd, buzzer)

keylock = KeyLock(hwalert, lcd)

pir = MotionSensor(config['MOTION_PIN'], sample_rate=5, queue_len=1)

mq2_alert = DigitalInputDevice(config['MQ2_DPIN'], pull_up=True)

picam = PiCamera()
