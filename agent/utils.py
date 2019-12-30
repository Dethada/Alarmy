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

class HWAlert():
    def __init__(self, buzzer_pin):
        self.bz = Buzzer(buzzer_pin)
        self.lcd = LCD()

    def on(self, msg):
        self.lcd.text('Alert', 1)
        self.lcd.text(msg, 2)
        self.bz.on()

    def off(self):
        self.bz.off()
        self.lcd.clear()
