import threading
from time import sleep
from nanpy import ArduinoApi, SerialManager
from gpiozero import Buzzer
import paho.mqtt.publish as publish
from rpi_lcd import LCD


class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


def nanpy_connect():
    connection = SerialManager(device='/dev/ttyUSB0')
    arduinoObject = ArduinoApi(connection=connection)
    return arduinoObject

def publish_single(topic, msg):
    publish.single(topic, msg, hostname="192.168.1.17")

class HWAlert():
    def __init__(self, buzzer_pin):
        self.bz = Buzzer(buzzer_pin)
        self.lcd = LCD()
        self._stop = False

    def on(self, msg):
        self.lcd.text('Alert', 1)
        self.lcd.text(msg, 2)
        self.bz.on()

    def off(self):
        print('Off ran')
        self.bz.off()
        self.lcd.clear()

    def _run_for(self, msg, time=0):
        self.on(msg)
        if time == 0:
          while True:
            sleep(1)
            if self._stop:
              break
        else:
          for i in range(time):
            sleep(1)
            if self._stop:
              break

        self.off()
    
    def run_for(self, msg, time=0):
        self.thread = Thread(self._run_for, msg, time)

    def kill(self):
        self.off()
        self._stop = True
        self.thread.join()
