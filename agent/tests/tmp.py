import io
from time import sleep
from base64 import b64encode
from picamera import PiCamera

picam = PiCamera()

def verify_person():
    frame = io.BytesIO()
    picam.capture(frame, format='jpeg')
    img_data = f'{b64encode(frame.getvalue()).decode()}'
    print(img_data)

verify_person()