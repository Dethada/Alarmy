from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_uri = "postgresql://alarmyuser:verysecurepassword123@192.168.1.17/alarmy"
engine = create_engine(db_uri)

Session = sessionmaker(engine)  
session = Session()