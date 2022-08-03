# Source: https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()

def fourImages(img):
    ActionList = []
    ActionList.append(handGesture(cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)))
    ActionList.append(handGesture(img))
    ActionList.append(handGesture(cv2.rotate(img, cv2.ROTATE_180)))
    ActionList.append(handGesture(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)))
    # print(ActionList)
    return ActionList


def handGesture(img):
    x, y, c = img.shape
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(imgrgb)
    className = ''

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(img, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model.predict([landmarks])
            classID = np.argmax(prediction)
            className = classNames[classID]
    
    if className == "peace" or className == "rock":
        return className


