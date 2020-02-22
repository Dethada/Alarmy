#!/usr/bin/env python3
import os
import base64
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

Base = declarative_base()

db_uri = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
db = create_engine(db_uri)


class Device(Base):
    __tablename__ = 'device'

    device_id = Column(String(32), primary_key=True)
    alarm = Column(Boolean, default=False, nullable=False)
    poll_interval = Column(Integer, nullable=False)
    alert_interval = Column(Integer, nullable=False)
    alarm_duration = Column(Integer, nullable=False)
    vflip = Column(Boolean, default=False, nullable=False)
    motd = Column(String(32), nullable=False)
    alarm_code = Column(String(16), nullable=False)
    detect_humans = Column(Boolean, nullable=False)
    temp_threshold = Column(Integer, nullable=False)


def main(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """

    if 'data' not in event:
        return
    device_id = base64.b64decode(event['data']).decode('utf-8')

    Session = sessionmaker(db)
    session = Session()

    device = Device(device_id=device_id, poll_interval=60, alert_interval=60, alarm_duration=60,
                    vflip=False, motd='Hello World', alarm_code='1234', detect_humans=False, temp_threshold=50)

    session.add(device)
    session.commit()

    print(f'Added device {device_id}')
