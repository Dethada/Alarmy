import os
from dotenv import load_dotenv
load_dotenv()

class Config():
    ALARM_DURATION = 60
    POLL_INTERVAL = 60
    ALERT_INTERVAL = 60
    TEMP_THRESHOLD = 50
    MQ2_APIN = int(os.getenv('MQ2_APIN'))
    MQ2_DPIN = int(os.getenv('MQ2_DPIN'))
    LM35_PIN = os.getenv('LM35_PIN')
    BUZZER_PIN = os.getenv('BUZZER_PIN')
    MOTION_PIN = os.getenv('MOTION_PIN')
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    WS_HOST = os.getenv('WS_HOST')
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    FROM_ADDR = 'alarmy@example.com'
    KEYPAD_CODE = '1234'
    MOTD = 'MOTD'
    VFLIP = False
    DETECT_HUMANS = False

config = Config()
