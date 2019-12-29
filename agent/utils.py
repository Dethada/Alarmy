import threading
from nanpy import ArduinoApi, SerialManager
from gpiozero import Buzzer
from rpi_lcd import LCD

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def nanpy_connect():
    connection = SerialManager(device='/dev/ttyUSB0')
    arduinoObject = ArduinoApi(connection=connection)
    return arduinoObject

def hardware_alert(msg):
    lcd = LCD()
    lcd.text('Alert!', 1)
    lcd.text(msg, 2)
    bz.on()