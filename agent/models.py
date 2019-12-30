from sqlalchemy import Column, BigInteger, DateTime, Float, ForeignKey, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    email = Column(String(320), primary_key=True)
    name = Column(String(100), nullable=False)
    role = Column(String(10), default='user', nullable=False)
    password = Column(String(80), nullable=False)
    get_alerts = Column(Boolean, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email


class EnvAlert(Base):
    __tablename__ = "env_alert"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    alert_time = Column(DateTime, default=datetime.now, nullable=False)
    reason = Column(String(100), nullable=False)
    gas_ticker = Column(BigInteger, ForeignKey('gas.ticker'), nullable=False)
    temp_ticker = Column(BigInteger, ForeignKey('temperature.ticker'), nullable=False)

    def __str__(self):
        return f'Alert at {self.alert_time}'


class Temperature(Base):
    __tablename__ = "temperature"

    ticker = Column(BigInteger, primary_key=True, autoincrement=True)
    value = Column(Float, nullable=False)
    capture_time = Column(DateTime, default=datetime.now,
                          unique=True, nullable=False)

    def __str__(self):
        return f'{self.value}C at {self.capture_time}'


class Gas(Base):
    __tablename__ = "gas"

    ticker = Column(BigInteger, primary_key=True, autoincrement=True)
    lpg = Column(Float, nullable=False)
    co = Column(Float, nullable=False)
    smoke = Column(Float, nullable=False)
    capture_time = Column(DateTime, default=datetime.now,
                          unique=True, nullable=False)

    def __str__(self):
        return f'{self.lpg}g PPM {self.co}g PPM {self.smoke}g PPM at {self.capture_time}'
