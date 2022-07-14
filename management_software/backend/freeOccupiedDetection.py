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

def freeOccupied(img):
    bbox, label, conf = cv.detect_common_objects(img)
    img = draw_bbox(img, bbox, label, conf)
    status = "Free"
    if "person" not in label:
        return status
    else: 
        for x in range(len(label)):
            if label[x] == 'person':
                status = "Occupied"
    return status
