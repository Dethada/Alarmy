import os
import base64
import json
from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, Float, ForeignKey, String, Boolean, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

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
    device_id = Column(String(64), ForeignKey('device.device_id'), nullable=False)
    value = Column(Float, nullable=False)
    capture_time = Column(DateTime, default=datetime.now,
                          unique=True, nullable=False)

    def str(self):
        return f'{self.value}C at {self.capture_time}'

class Gas(Base):
    __tablename__ = "gas"

    ticker = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(String(64), ForeignKey('device.device_id'), nullable=False)
    lpg = Column(Float, nullable=False)
    co = Column(Float, nullable=False)
    smoke = Column(Float, nullable=False)
    capture_time = Column(DateTime, default=datetime.now,
                          unique=True, nullable=False)

    def str(self):
        return f'{self.lpg}g PPM {self.co}g PPM {self.smoke}g PPM at {self.capture_time}'

class EnvAlert(Base):
    __tablename__ = "env_alert"

    cid = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(String(64), ForeignKey('device.device_id'), nullable=False)
    alert_time = Column(DateTime, default=datetime.now, nullable=False)
    reason = Column(String(100), nullable=False)
    gas_ticker = Column(BigInteger, ForeignKey('gas.ticker'), nullable=False)
    temp_ticker = Column(BigInteger, ForeignKey('temperature.ticker'), nullable=False)

    def str(self):
        return f'Alert at {self.alert_time}'

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
    attrdict = event.get("attributes")
    device_id = attrdict.get("deviceId")
    alert_time = data.get("time")

    reason = ""
    subfolder = attrdict.get("subFolder")
    if subfolder == "alerts/gas":
        reason += "Gases Detected"
    elif subfolder == "alerts/temp":
        reason += "High Temperature"
        
    Session = sessionmaker(db)
    session = Session()
    temperature = Temperature(device_id=device_id, value=data.get("temp"), capture_time=alert_time)
    gas = Gas(device_id=device_id,lpg=gasdict.get("lpg"),co=gasdict.get("co"),smoke=gasdict.get("smoke"),capture_time=alert_time)
    session.add(temperature)
    session.add(gas)
    session.commit()

    gas_ticker = session.query(Gas).filter(Gas.capture_time == alert_time).first().ticker
    temp_ticker = session.query(Temperature).filter(Temperature.capture_time == alert_time).first().ticker
    
    envalert = EnvAlert(device_id=device_id,alert_time=alert_time,reason=reason,gas_ticker=gas_ticker,temp_ticker=temp_ticker)
    session.add(envalert)
    session.commit()
