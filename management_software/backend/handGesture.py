# Source: https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import csv
from model import KeyPointClassifier
import copy
import itertools




# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.85)
mpDraw = mp.solutions.drawing_utils
keypoint_classifier = KeyPointClassifier()
# Load the gesture recognizer model
# model = load_model('C:\\Users\\patrick\\Documents\\ENSC405-Capstone\\management_software\\backend\\keypoint_classifier.hdf5')
with open('model/keypoint_classifier/keypoint_classifier_label.csv',
            encoding='utf-8-sig') as f:
    keypoint_classifier_labels = csv.reader(f)
    keypoint_classifier_labels = [
        row[0] for row in keypoint_classifier_labels
    ]
mode = 0

# Load class names
# with open('keypoint_classifier_label.csv',
#             encoding='utf-8-sig') as f:
#     keypoint_classifier_labels = csv.reader(f)
#     keypoint_classifier_labels = [
#         row[0] for row in keypoint_classifier_labels
#     ]
# f = open('gesture.names', 'r')
# classNames = f.read().split('\n')
# f.close()

def fourImages(img):
    ActionList = []
    # ActionList.append(handGesture(cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)))
    ActionList.append(handGesture(img))
    # ActionList.append(handGesture(cv2.rotate(img, cv2.ROTATE_180)))
    # ActionList.append(handGesture(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)))
    ActionList = list(filter(None, ActionList))
    # print(ActionList)
    return ActionList
# mode = 0

def handGesture(img):
    className =''
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    debug_image = copy.deepcopy(img)
    results = hands.process(image)
    if results.multi_hand_landmarks is not None:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
            landmark_list = calc_landmark_list(debug_image, hand_landmarks)
            pre_processed_landmark_list = pre_process_landmark(landmark_list)
            hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
            className = keypoint_classifier_labels[hand_sign_id]
            print (className)
    return className
                                                  
    # imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # result = hands.process(imgrgb)
    # className = ''

    # # post process the result
    # if result.multi_hand_landmarks:
    #     landmarks = []
    #     for handslms in result.multi_hand_landmarks:
    #         for lm in handslms.landmark:
    #             lmx = int(lm.x * x)
    #             lmy = int(lm.y * y)

    #             landmarks.append([lmx, lmy])

    #         # Drawing landmarks on frames
    #         mpDraw.draw_landmarks(img, handslms, mpHands.HAND_CONNECTIONS)

    #         # Predict gesture
    #         prediction = model.predict([landmarks])
    #         print("Max prediction , ", prediction.max())
    #         print(np.argmax(prediction))
    #         if prediction.max() >= .85:
    #             print("inside If")
    #             classID = np.argmax(prediction)
    #             className = classNames[classID]
    #             print(className)
    #         else:
    #             continue

    # return className



    # className = ''
    # classNames = hands.process(img)
    # return classNames
def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point