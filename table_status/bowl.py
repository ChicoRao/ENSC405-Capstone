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

url='http://192.168.1.75/capture?_cb=1649748796132'

# classNames= []
# classFile = 'coco.names'
# with open(classFile,'rt') as f:
#     classNames = f.read().rstrip('\n').split('\n')
# print(classNames)

# configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
# weightsPath = 'frozen_inference_graph.pb'

# net = cv2.dnn_DetectionModel(weightsPath,configPath)
# net.setInputSize(320,320)
# net.setInputScale(1.0/ 127.5)
# net.setInputMean((127.5, 127.5, 127.5))
# net.setInputSwapRB(True)

async def bowl(imgcopy, bbox):
    x1 = bbox[0]
    y1 = bbox[1]
    w1 = bbox[2]
    h1 = bbox[3]
    cv2.rectangle(imgcopy, (x1,y1), (w1,h1), (255,0,0), 2)
    crop_img = imgcopy[y1:h1, x1:w1]
    height, width = crop_img.shape[:2]

    if not crop_img.all():
        #gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        #blurred = cv2.GaussianBlur(gray,(7,7),0) #try do it first, then go to "gray"

        blurred = cv2.GaussianBlur(crop_img,(7,7),0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        (T, threshInv) = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow('gray',threshInv)
        contours, hierarchy = cv2.findContours(threshInv,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(imgcopy, contours, -1, (0, 255, 0), 2)
        if( hierarchy is not None):
            number_of_contours = len(hierarchy[0])
            #print(number_of_contours)
            if number_of_contours >= 4:
                #cv2.rectangle(imgcopy, (x1-10,y1-10), (w1-10,h1-10), (0, 10, 255), 2)
                cv2.drawContours(crop_img, contours, -1, (0, 10, 255), 2)
                cv2.putText(imgcopy,"Food",(x1+10,y1-20),cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
    return(imgcopy)

async def run1():
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)

    while True:
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img = cv2.imdecode(imgnp,-1)
        imgcopy = img.copy()
        bbox, label, conf = cv.detect_common_objects(img)
        img = draw_bbox(img, bbox, label, conf)
        result = imgcopy.copy()

        for x in range(len(label)):
            if label[x] == 'sink' or label[x] == 'bowl' or label[x] == 'toilet':
                result = await bowl(imgcopy,bbox[x])
    
    # classIds, confs, bbox = net.detect(img,confThreshold=0.5)
        
    # if len(classIds) != 0:
    #     for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
    #         cv2.rectangle(img,box,color=(0,255,0),thickness=2)
    #         cv2.putText(img,classNames[classId-1],(box[0]+10,box[1]-20),cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    # contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(imgcopy, contours, -1, (0, 255, 0), 2)

    # for box, lab, confidence in zip(bbox, label, conf):
    #     cv2.rectangle(img,box,color=(0,255,0),thickness=2)
    #     cv2.putText(img,"Food",(box[0]+10,box[1]-20),cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

        #bit = cv2.bitwise_and(img,result)
        #cv2.imshow('detection',bit)
        cv2.imshow('detection',img)
        cv2.imshow('result',result)
        key=cv2.waitKey(5)
        if key==ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("started")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run1())
   