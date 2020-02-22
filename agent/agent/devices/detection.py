#!/usr/bin/env python3
import io
from time import sleep
from time import time
from base64 import b64encode
from picamera import PiCamera
from utils import get_current_time
from comms import publish
from devices import hwalert, pir, picam
from config import config
from google.cloud import storage

def upload_blob(data,timestamp):
    # Default credentials fix: https://stackoverflow.com/questions/42043611/could-not-load-the-default-credentials-node-js-google-compute-engine-tutorial
    storage_client = storage.Client()
    bucket = storage_client.bucket("alarmy-person-images")
    filename = f"{timestamp}.jpg"
    blob = bucket.blob(filename)
    blob.upload_from_string(data,content_type='image/jpeg')
    print("File uploaded to {}.".format(filename))

def verify_person():
    if not config['DETECT_HUMANS']:
        return
    frame = io.BytesIO()
    picam.capture(frame, format='jpeg')
    img_data = frame.getvalue()
    timestamp = int(time())
    upload_blob(img_data,timestamp)

def detect_humans():
    pir.when_motion=verify_person

    # clear the camera buffer
    # while True:
    #     capture.read()
    #     sleep(0.1)
