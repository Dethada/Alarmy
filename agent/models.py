from sqlalchemy import Column, BigInteger, DateTime, Float, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


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
