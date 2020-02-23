#!/usr/bin/env python3
# Adapted from https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/TFLite_detection_image.py
import os
import json
from datetime import datetime
import requests
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import storage
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, ForeignKey, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from utils.notifyer import broadcast_mail
# from db import session
# from devices import hwalert, pir, capture
# from utils.sensor import trigger_alert_helper

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

Base = declarative_base()


class Device(Base):
    __tablename__ = 'device'

    device_id = Column(String(64), primary_key=True)
    alarm = Column(Boolean, default=False, nullable=False)
    poll_interval = Column(Integer, nullable=False)
    alert_interval = Column(Integer, nullable=False)
    alarm_duration = Column(Integer, nullable=False)
    vflip = Column(Boolean, default=False, nullable=False)
    motd = Column(String(32), nullable=False)
    alarm_code = Column(String(16), nullable=False)
    detect_humans = Column(Boolean, nullable=False)
    temp_threshold = Column(Integer, nullable=False)


class PersonAlert(Base):
    __tablename__ = "person_alert"

    cid = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(String(64), ForeignKey(
        'device.device_id'), nullable=False)
    alert_time = Column(DateTime, default=datetime.now, nullable=False)
    image = Column(String(255), nullable=False)

    def __str__(self):
        return '<Person alert at %r>' % self.alert_time


db_uri = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
db = create_engine(db_uri)


def detect_human(content):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    image = types.Image(content=content)

    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    for object_ in objects:
        if object_.name == 'Person' and object_.score > 0.5:
            print('\n{} (confidence: {})'.format(object_.name, object_.score))
            # print('Normalized bounding polygon vertices: ')
            # for vertex in object_.bounding_poly.normalized_vertices:
            #     print(' - ({}, {})'.format(vertex.x, vertex.y))
            return True
    return False


def download_blob(bucket_name, source_blob_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    return blob.download_as_string()



def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()


def main(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    bucket_name,img_path = data['bucket'], data['name']
    img_bytes = download_blob(bucket_name, img_path)
    if not detect_human(img_bytes):
        delete_blob(bucket_name, img_path)
        print("Blob {} deleted.".format(img_path))
        return
    device_id = img_path.split('/')[0]
    img_url = f"https://storage.googleapis.com/{bucket_name}/{img_path}"
    Session = sessionmaker(db)
    session = Session()

    person = PersonAlert(device_id=device_id, alert_time=data['timeCreated'], image=img_url)

    session.add(person)
    session.commit()
