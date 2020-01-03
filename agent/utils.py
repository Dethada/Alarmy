import threading
from nanpy import ArduinoApi, SerialManager


class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


def nanpy_connect():
    connection = SerialManager(device='/dev/ttyUSB0')
    arduinoObject = ArduinoApi(connection=connection)
    return arduinoObject

def publish_single(topic, msg):
    publish.single(topic, msg, hostname="192.168.1.103")
