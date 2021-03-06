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
import torch
from PIL import Image

im=None

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

Plate = Blueprint('Plate',__name__)

@Plate.route("/Plate")
def plateStatus(img,box,status):
    x1 = box[0]
    y1 = box[1]
    w1 = box[2]
    h1 = box[3]
    cv2.rectangle(img, (x1,y1), (w1,h1), (255,0,0), 2)
    crop_img = img[y1:h1, x1:w1]

    statusPlate = status

    # For testing
    #cv2.imshow("crop_img", crop_img)

    if not crop_img.all():
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(7,7),0)
        ret, thresh = cv2.threshold(blurred, 127, 255, 0)
        #cv2.imshow("edges", edges)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print(len(hierarchy[0]))
        number_of_contours = len(hierarchy[0])
        if number_of_contours >= 5:
            statusPlate = "Food"
        else:
            statusPlate = "Dirty"
    return (statusPlate)


def run3(img):

    try:
        box, label, conf = model(img)
        img = draw_bbox(img, box, label, conf)
        for x in range(len(label)):
            if label[x] == 'Plate':
                status = plateStatus(img,box[x],status)
    except:
        # not found
        status = "No Plate"

    
    
    # # cv2.imshow("image", img)
    # if "Plate" not in label:
    #     return status
    # else: 
        
    return status