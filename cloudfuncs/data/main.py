import os
import base64
import json
from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, Float, ForeignKey, String, Boolean, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

BACKEND = os.getenv('BACKEND')
SERVICE_USER = os.getenv('SERVICE_USER')
SERVICE_PASS = os.getenv('SERVICE_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

Base = declarative_base()

db_uri = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
db = create_engine(db_uri)


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


class Temperature(Base):
    __tablename__ = "temperature"

    ticker = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(String(64), ForeignKey(
        'device.device_id'), nullable=False)
    value = Column(Float, nullable=False)
    capture_time = Column(DateTime, default=datetime.now,
                          unique=True, nullable=False)

    def str(self):
        return f'{self.value}C at {self.capture_time}'


class Gas(Base):
    __tablename__ = "gas"

    ticker = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(String(64), ForeignKey(
        'device.device_id'), nullable=False)
    lpg = Column(Float, nullable=False)
    co = Column(Float, nullable=False)
    smoke = Column(Float, nullable=False)
    capture_time = Column(DateTime, default=datetime.now,
                          unique=True, nullable=False)

    def str(self):
        return f'{self.lpg}g PPM {self.co}g PPM {self.smoke}g PPM at {self.capture_time}'


def get_token(host):
    r = requests.post(f'{host}/token/auth', json={'email': SERVICE_USER,
                                                  'pass': SERVICE_PASS})
    return r.json()['access_token']


def newValues(host, token):
    r = requests.post(f'{host}/hooks/data',
                      headers={"Authorization": f"Bearer {token}"})
    return r.status_code == 200


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
    msg_body = base64.b64decode(event.get("data")).decode('utf-8')
    data = json.loads(msg_body)
    gasdict = data.get('gas')
    device_id = event['attributes']["deviceId"]
    Session = sessionmaker(db)
    session = Session()

    print(f'Device ID: {device_id}')
    temperature = Temperature(device_id=device_id, value=data.get(
        "temp"), capture_time=data.get("time"))
    gas = Gas(device_id=device_id, lpg=gasdict.get("lpg"), co=gasdict.get(
        "co"), smoke=gasdict.get("smoke"), capture_time=data.get("time"))
    try:
        session.add(temperature)
        session.add(gas)
        session.commit()
        if newValues(BACKEND, get_token(BACKEND)):
            print('Notified clients')
        else:
            print('Failed to notify clients')
    except IntegrityError:
        print('Device is not registered')
