from datetime import datetime
from .extensions import db


class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(320), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), default='user', nullable=False)
    password = db.Column(db.String(80), nullable=False)
    get_alerts = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email


class PersonAlert(db.Model):
    __tablename__ = "person_alert"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    alert_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    image = db.Column(db.Text, nullable=False)

    def __str__(self):
        return '<Person alert at %r>' % self.alert_time


class EnvAlert(db.Model):
    __tablename__ = "env_alert"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    alert_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    gas_ticker = db.Column(db.BigInteger, db.ForeignKey('gas.ticker'), nullable=False)
    temp_ticker = db.Column(db.BigInteger, db.ForeignKey('temperature.ticker'), nullable=False)
    gas = db.relationship("Gas", backref=db.backref("env_alert", uselist=False), lazy=True)
    temperature = db.relationship("Temperature", backref=db.backref("env_alert", uselist=False), lazy=True)

    def __str__(self):
        return f'Alert at {self.alert_time}'

class Temperature(db.Model):
    __tablename__ = 'temperature'

    ticker = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    value = db.Column(db.Float, nullable=False)
    capture_time = db.Column(db.DateTime, default=datetime.now, unique=True, nullable=False)

    def __repr__(self):
        return '<Temp Tick %r>' % self.ticker

class Gas(db.Model):
    __tablename__ = 'gas'

    ticker = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    lpg = db.Column(db.Float, nullable=False)
    co = db.Column(db.Float, nullable=False)
    smoke = db.Column(db.Float, nullable=False)
    capture_time = db.Column(db.DateTime, default=datetime.now, unique=True, nullable=False)

    def __repr__(self):
        return '<Gas Tick %r>' % self.ticker
