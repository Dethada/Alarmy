#!/usr/bin/env python3
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
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
    get_alerts = Column(Boolean, default=False, nullable=False)
    # device_id = Column(String(32), ForeignKey('device.device_id'), nullable=True)


Session = sessionmaker(engine)
session = Session()

ph = PasswordHasher()
default_user = User(email='admin@admin.com', name='Default Admin',
                    role='Admin', password=ph.hash('password'))
service_user = User(email='service@service.hiding.icu', name='Service Account',
                    role='Service', password=ph.hash('Tdrw#o@upN^Gyj5HnEv9n4F$cE9YBfR!s'))

session.add(default_user)
session.add(service_user)
session.commit()

print('Done')
