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
    thresh = 200

    bbox, label, conf = cv.detect_common_objects(img)
    img = draw_bbox(img, bbox, label, conf)
    status = "no_plates"
    if "plate" not in label:
        return status
    else: 
        for x in range(len(label)):
            if label[x] ==  "plate":
                status = "has_plate"
                # gray = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
                # edges = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
                # #convert the image to grayscale
                # cv2.CvtColor(img, gray, cv.CV_BGR2GRAY)
                # #edge detect it, then smooth the edges
                # cv2.Canny(gray, edges, thresh, thresh / 2, 3)
                # cv2.Smooth(gray, gray, cv.CV_GAUSSIAN, 3, 3) 

                # object_in_plate = 0
                # _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

                # for contour in contours:
                #     object_in_plate = object_in_plate + 1
                import cv2 as cv
                #read the image
                #convert the image to grayscale
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                #blur image to reduce the noise in the image while thresholding. #This smoothens the sharp edges in the image.
                blur = cv.blur(gray, (10,10))
                #Apply thresholding to the image
                ret, thresh = cv.threshold(blur, 1, 255, cv.THRESH_OTSU)
                #find the contours in the image
                contours, heirarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                #draw the obtained contour lines(or the set of coordinates forming a line) on the original image
                cv.drawContours(img, contours, -1, (0,255,0), 20)
                #show the image
                cv.namedWindow('Contours',cv.WINDOW_NORMAL)
                cv.namedWindow('Thresh',cv.WINDOW_NORMAL)
                cv.imshow('Contours', img)
                cv.imshow('Thresh', thresh)
                if cv.waitKey(0):
                    cv.destroyAllWindows()