from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config

db_uri = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"
engine = create_engine(db_uri)

Session = sessionmaker(engine)  
session = Session()