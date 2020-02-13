from time import sleep
from utils import Thread, write_config
from config import config


class HWAlert():
    def __init__(self, lcd, buzzer):
        self.bz = buzzer
        self.lcd = lcd
        self._stop = False
        self.thread = None
        self.msg = None
        self.lcd.clear()
        self.lcd.text(config['MOTD'], 1)

    def on(self, msg):
        self.msg = msg
        self.lcd.text('Alert', 1)
        self.lcd.text(self.msg, 2)
        self.bz.on()

    def off(self):
        self.bz.off()
        self.msg = None
        self.lcd.clear()
        self.lcd.text(config['MOTD'], 1)

    def _run_for(self, msg, time=0):
        self._stop = False
        self.on(msg)
        if time == 0:
            while True:
                sleep(1)
                if self._stop:
                    config['ALARM_ON'] = False
                    write_config()
                    break
        else:
            for i in range(time):
                sleep(1)
                if self._stop:
                    config['ALARM_ON'] = False
                    write_config()
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
