#!/usr/bin/env python3
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean
from argon2 import PasswordHasher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

db_uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(db_uri)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    email = Column(String(320), primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    role = Column(String(10), default='user', nullable=False)
    password = Column(String(80), nullable=False)


class Device(Base):
    __tablename__ = 'device'

    cid = Column(Integer, primary_key=True, autoincrement=True)
    alarm = Column(Boolean, default=False, nullable=False)
    poll_interval = Column(Integer, nullable=False)
    alert_interval = Column(Integer, nullable=False)
    alarm_duration = Column(Integer, nullable=False)
    email = Column(String(320), nullable=False)
    vflip = Column(Boolean, default=False, nullable=False)
    motd = Column(String(32), nullable=False)
    alarm_code = Column(String(16), nullable=False)
    detect_humans = Column(Boolean, nullable=False)
    temp_threshold = Column(Integer, nullable=False)


Session = sessionmaker(engine)
session = Session()

ph = PasswordHasher()
default_user = User(email='admin@admin.com', name='Default Admin',
                    role='Admin', password=ph.hash('password'))
device = Device(poll_interval=60, alert_interval=60, alarm_duration=60, email='alarmy@hiding.icu',
                vflip=False, motd='Hello World', alarm_code='1234', detect_humans=False, temp_threshold=50)

session.add(default_user)
session.add(device)
session.commit()

print('Done')
