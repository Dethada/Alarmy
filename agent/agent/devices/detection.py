#!/usr/bin/env python3
import io
from time import sleep
from base64 import b64encode
from picamera import PiCamera
from utils.general import publish, get_current_time
from devices import hwalert, pir, picam
from config import config

def verify_person():
    if not config['DETECT_HUMANS']:
        return
    frame = io.BytesIO()
    picam.capture(frame, format='jpeg')
    img_data = f'{b64encode(frame.getvalue()).decode()}'
    current_time = get_current_time()
    publish("alerts/motion", {"time":current_time, "image": img_data})


def detect_humans():
    pir.when_motion=verify_person

    # clear the camera buffer
    # while True:
    #     capture.read()
    #     sleep(0.1)
