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

url='http://10.0.0.102/capture?_cb=1649020515981'
im=None

plate = Blueprint('plate',__name__)

@plate.route("/plate")


def dirtyPlate(img,bbox,status):
    x1 = bbox[0]
    y1 = bbox[1]
    w1 = bbox[2]
    h1 = bbox[3]
    cv.rectangle(img, (x1,y1), (w1,h1), (255,0,0), 2)
    crop_img = img[y1:h1, x1:w1]

    statusPlate = status

    # For testing
    cv2.imshow("crop_img", crop_img)

    if not crop_img.all():
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(7,7),0)
        (T, threshInv) = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (w1,1))
        horizontal_mask = cv2.morphologyEx(threshInv, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
        edges = cv2.Canny(horizontal_mask,60, 80)
        #cv2.imshow("edges", edges)
        contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print(len(hierarchy[0]))
        number_of_contours = len(hierarchy[0])
        if number_of_contours >= 4:
            statusPlate = "Dirty"
        else:
            statusPlate = "Clean"
    return (statusPlate)


def run2(img):

    bbox, label, conf = cv.detect_common_objects(img)
    img = draw_bbox(img, bbox, label, conf)
    status = "No Plate"
    # cv2.imshow("image", img)
    if "plate" not in label:
        return status
    else: 
        for x in range(len(label)):
            if label[x] == 'plate':
                status = dirtyPlate(img,bbox[x],status)
    return status
                