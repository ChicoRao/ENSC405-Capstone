from flask import Blueprint
from tracemalloc import start
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import urllib.request
import numpy as np
import sys
from cvlib.object_detection import draw_bbox
import concurrent.futures
import math
import asyncio
import time 




def dirtyPlate(img):
    _, frame = cap.read()
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([38, 86, 0])
    upper_blue = np.array([121, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    bbox, label, conf = cv.detect_common_objects(img)
    img = draw_bbox(img, bbox, label, conf)
    status = "no_plates"
    if "plate" not in label:
        return status
    else: 
        for x in range(len(label)):
            if label[x] ==  "plate":
                status = "has_plate"
                gray = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
                edges = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
                #convert the image to grayscale
                cv2.CvtColor(img, gray, cv.CV_BGR2GRAY)
                #edge detect it, then smooth the edges
                cv2.Canny(gray, edges, thresh, thresh / 2, 3)
                cv2.Smooth(gray, gray, cv.CV_GAUSSIAN, 3, 3) 

                object_in_plate = 0
                _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

                for contour in contours:
                    object_in_plate = object_in_plate + 1
