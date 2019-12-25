#!/usr/bin/env python3
from typing import Optional
import numpy as np
import cv2

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# open webcam video stream
cap = cv2.VideoCapture(0)


def detect_person(src_frame: np.ndarray) -> Optional[np.ndarray]:
    """Detect if a person is in a frame.

    Args:
        src_frame (ndarray): The first parameter.

    Returns:
        (ndarray, optional): The return value. True for success, False otherwise.

    """
    # resizing for faster detection
    frame = cv2.resize(src_frame, (640, 480))
    # using a greyscale picture, also for faster detection
    # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    if boxes.any():
        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)

        return frame
    return None


print('Started...')
while True:
    # Capture frame-by-frame
    _, frame = cap.read()
    res = detect_person(frame)
    if res is not None:
        print('Person detected!')
        cv2.imwrite("out.jpg", res)
        break

# When everything done, release the capture
cap.release()
