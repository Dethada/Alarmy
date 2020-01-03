import os
from dotenv import load_dotenv
load_dotenv()

class Config():
    ALARM_DURATION = 60
    POLL_INTERVAL = 60
    ALERT_INTERVAL = 60
    MQ2_PIN = int(os.getenv('MQ2_PIN'))
    LM35_PIN = os.getenv('LM35_PIN')
    BUZZER_PIN = os.getenv('BUZZER_PIN')
    MOTION_PIN = os.getenv('MOTION_PIN')
    FROM_ADDR = os.getenv('FROM_ADDR')
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    VFLIP = False

config = Config()