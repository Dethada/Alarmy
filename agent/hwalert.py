from time import sleep
from rpi_lcd import LCD
from gpiozero import Buzzer
from utils import Thread
from config import config


class HWAlert():
    def __init__(self, buzzer_pin):
        self.bz = Buzzer(buzzer_pin)
        self.lcd = LCD()
        self._stop = False
        self.thread = None
        self.msg = None
        self.lcd.clear()
        self.lcd.text(config.MOTD, 1)

    def on(self, msg):
        self.msg = msg
        self.lcd.text('Alert', 1)
        self.lcd.text(self.msg, 2)
        self.bz.on()

    def off(self):
        self.bz.off()
        self.msg = None
        self.lcd.clear()
        self.lcd.text(config.MOTD, 1)

    def _run_for(self, msg, time=0):
        self._stop = False
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

    def stop_alert(self):
        self.off()
        self._stop = True
        if self.thread:
            self.thread.join()
        self.thread = None


hwalert = HWAlert(config.BUZZER_PIN)
