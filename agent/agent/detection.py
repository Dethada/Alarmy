#!/usr/bin/env python3
# Modified from
# https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/TFLite_detection_image.py
import os
import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter
from datetime import datetime
from base64 import b64encode
from models import PersonAlert, Device
from notifyer import broadcast_mail
from events import ws_notify_users
from db import session
from devices import hwalert, pir
from config import config
from time import sleep

MODEL_NAME = 'ssd_mobilenet/'
GRAPH_NAME = 'detect.tflite'
LABELMAP_NAME = 'labelmap.txt'
min_conf_threshold = 0.5

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def detect_person_frame(image):
    # Load image and resize to expected shape [1xHxWx3]
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape 
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
    #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)

    detected = False
    # Loop over all detections and draw detection box if detected object is a person and confidence is above minimum threshold
    for i in range(len(scores)):
        if classes[i] == 0 and scores[i] > min_conf_threshold and scores[i] <= 1.0:
            detected = True
            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
            
            cv2.rectangle(image, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

            # Draw label
            label = 'person: %d%%' % (int(scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

    if detected:
        return image
    return None

def insert_data(img_data):
    current_time = datetime.now()
    person_alert = PersonAlert(image=img_data, alert_time=current_time)
    session.add(person_alert)
    session.commit()
    return current_time

def verify_person():
    if not config.DETECT_HUMANS:
        print('Aborted')
        return
    _, frame = cap.read()
    if config.VFLIP:
        frame = cv2.flip(frame, 0)
    res = detect_person_frame(frame)
    if res is not None:
        print('Person detected')
        # sound buzzer & save frame to img & send notification
        _, buffer_img = cv2.imencode('.jpg', res)
        img_data = f'{b64encode(buffer_img).decode()}'
        alert_time = insert_data(img_data)
        print('Person detected')
        msg = {'subject': 'Person detected', 'content': f'Person detected at {alert_time}<br><img src="cid:defaultcid"/>', 'img_attachment': img_data}
        ws_notify_users('Person detected!')
        device = session.query(Device).first()
        device.alarm= True
        session.commit()
        hwalert.run_for('Person Detected', config.ALARM_DURATION)
        broadcast_mail(msg)
        sleep(config.ALERT_INTERVAL)


def detect_humans():
    pir.when_motion=verify_person

    # clear the camera buffer
    while True:
        cap.read()
