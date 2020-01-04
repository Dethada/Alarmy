#!/usr/bin/env python3
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, DateTime, Float, create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

db_uri = "postgresql://alarmyuser:verysecurepassword123@192.168.1.103/alarmy"
engine = create_engine(db_uri)


Base = declarative_base()


class Temperature(Base):
    __tablename__ = "temperature"
    
    ticker = Column(BigInteger, primary_key=True, autoincrement=True)
    value = Column(Float, nullable=False)
    capture_time = Column(DateTime, default=datetime.now, unique=True, nullable=False)

    def __str__(self):
        return f'{self.value}C at {self.capture_time}'


class Gas(Base):
    __tablename__ = "gas"

    ticker = Column(BigInteger, primary_key=True, autoincrement=True)
    lpg = Column(Float, nullable=False)
    co = Column(Float, nullable=False)
    smoke = Column(Float, nullable=False)
    capture_time = Column(DateTime, default=datetime.now, unique=True, nullable=False)

    def __str__(self):
        return f'{self.lpg}g PPM {self.co}g PPM {self.smoke}g PPM at {self.capture_time}'

Session = sessionmaker(engine)  
session = Session()

def get_24h_temp_data():
    since = datetime.now() - timedelta(hours=24)

    df = pd.read_sql(session.query(Gas).filter(Gas.capture_time > since).statement, session.bind)
    df['capture_time'] = pd.to_datetime(df['capture_time'])
    df.index = df['capture_time']
    df = df.resample('H').mean().dropna()
    result = [(time, value) for time, value in zip(df.index, df['value'])]
    result = []
    for row in df.itertuples():
        print(row.Index, row.lpg, row.co, row.smoke)

    # print(result)

def get_7days_temp_data():
    since = datetime.now() - timedelta(days=7)

    df = pd.read_sql(session.query(Temperature).filter(Temperature.capture_time > since).statement, session.bind)
    df['capture_time'] = pd.to_datetime(df['capture_time'])
    df.index = df['capture_time']

    print(df.resample('4H').mean())

def get_30days_temp_data():
    since = datetime.now() - timedelta(days=30)

    df = pd.read_sql(session.query(Temperature).filter(Temperature.capture_time > since).statement, session.bind)
    df['capture_time'] = pd.to_datetime(df['capture_time'])
    df.index = df['capture_time']

    print(df.resample('D').mean())

def get_all_temp_data():
    df = pd.read_sql(session.query(Temperature).statement, session.bind)
    df['capture_time'] = pd.to_datetime(df['capture_time'])
    df.index = df['capture_time']

    print(df.resample('2W').mean())

get_24h_temp_data()