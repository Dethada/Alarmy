#!/usr/bin/env python3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from argon2 import PasswordHasher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_uri = "postgresql://alarmyuser:verysecurepassword123@192.168.1.17/alarmy"
engine = create_engine(db_uri)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    email = Column(String(320), primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    role = Column(String(10), default='user', nullable=False)
    password = Column(String(80), nullable=False)

Session = sessionmaker(engine)  
session = Session()

ph = PasswordHasher()
default_user = User(email='admin@admin.com', name='Default Admin', role='Admin', password=ph.hash('password'))

session.add(default_user)
session.commit()

# select *
result = engine.execute('SELECT * FROM '
                        '"users"')
for _r in result:
    print(_r)

# result = engine.execute('SELECT * FROM "EX1"')
# print(result.fetchall())
