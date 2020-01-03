#!/usr/bin/env python3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean
from argon2 import PasswordHasher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_uri = "postgresql://alarmyuser:verysecurepassword123@192.168.1.103/alarmy"
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    alarm = Column(Boolean, default=False, nullable=False)
    poll_interval = Column(Integer, nullable=False)
    alert_interval = Column(Integer, nullable=False)
    alarm_duration = Column(Integer, nullable=False)
    email = Column(String(320), nullable=False)
    vflip = Column(Boolean, default=False, nullable=False)

Session = sessionmaker(engine)  
session = Session()

ph = PasswordHasher()
default_user = User(email='admin@admin.com', name='Default Admin', role='Admin', password=ph.hash('password'))
device = Device(poll_interval=60, alert_interval=60, alarm_duration=60, email='alarmy@hiding.icu', vflip=False)

# session.add(default_user)
session.add(device)
session.commit()

# select *
# result = engine.execute('SELECT * FROM '
#                         '"users"')
# for _r in result:
#     print(_r)

# result = engine.execute('SELECT * FROM "EX1"')
# print(result.fetchall())
print('Done')