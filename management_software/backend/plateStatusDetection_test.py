from tracemalloc import start
import cv2 
import matplotlib.pyplot as plt
import cvlib as cv
import numpy as np
import sys
from cvlib.object_detection import draw_bbox

import torch
from PIL import Image

im=None

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

def plateStatus():
    img = cv2.imread('base_photo_.png')

    print ("111111111111111111111111")
    result = model(img)
    print ("222222222222222222222222")
    crops = result.crop(save=True)
    print ("333333333333333333333333")
    
    print ("4444444444444444444444444")

    cv2.imshow('detection',img)




    statusPlate = "No Plate"

    # For testing
    #cv2.imshow("crop_img", crop_img)

    if not crops.all():
        gray = cv2.cvtColor(crops, cv2.COLOR_BGR2GRAY)
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
    print (statusPlate)
    return (statusPlate)
    


def main():
    plateStatus()

if __name__ == "__main__":
    main()

    # try:
    #     box, label, conf = model(img)
    #     img = draw_bbox(img, box, label, conf)
    #     for x in range(len(label)):
    #         if label[x] == 'Plate':
    #             status = plateStatus(img,box[x],status)
    # except:
    #     # not found
    #     status = "No Plate"

    
    
    # # cv2.imshow("image", img)
    # if "Plate" not in label:
    #     return status
    # else: 
        
    #return status