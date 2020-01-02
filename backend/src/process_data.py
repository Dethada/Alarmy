#!/usr/bin/env python3
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, DateTime, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_uri = "postgresql://alarmyuser:verysecurepassword123@192.168.1.17/alarmy"
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

result = session.query(Gas)
# select *
result = engine.execute('SELECT * FROM '
                        '"users"')
for _r in result:
    print(_r)

# result = engine.execute('SELECT * FROM "EX1"')
# print(result.fetchall())
