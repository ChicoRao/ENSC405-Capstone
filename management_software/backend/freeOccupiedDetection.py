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


def gaussian_kernel(dimension_x, dimension_y, sigma_x, sigma_y):
    x = cv2.getGaussianKernel(dimension_x, sigma_x)
    y = cv2.getGaussianKernel(dimension_y, sigma_y)
    kernel = x.dot(y.T)
    return kernel


    # g_kernel = gaussian_kernel(5, 5, 1, 1)

def freeOccupied(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = gaussian_kernel(5,5,1,1)
    bbox, label, conf = cv.detect_common_objects(img)
    img = draw_bbox(img, bbox, label, conf)
    status = "Free"
    print(label)
    if "person" not in label:
        return status
    else: 
        for x in range(len(label)):
            if label[x] == 'person':
                status = "Occupied"
    return status
