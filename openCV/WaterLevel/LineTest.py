from tracemalloc import start
import cv2
import cvlib as cv
import numpy as np
import sys
from cvlib.object_detection import draw_bbox
import math

#reading image from file
#does not work with cup 1
#works with cup 2,3,4,5
#kind of works with cup 11

#img = cv2.imread(r'C:\Users\<username>\Desktop\ENSC405-Capstone\openCV\WaterLevel') #might need to change the path

img = cv2.imread(r'C:\Users\Angus\Desktop\ENSC405-Capstone\openCV\WaterLevel\cup4.png') #might need to change the path

#detecting the objects in the image
bbox, label, conf = cv.detect_common_objects(img)
im = draw_bbox(img, bbox, label, conf)

cv2.imshow('detection',im)

#grab the dimensions of the cup
print(bbox[0])
x1 = bbox[0][0]
y1 = bbox[0][1]
w1 = bbox[0][2]
h1 = bbox[0][3]

#executes this only if the object detected is a cup
if label[0] == 'cup':

    #drawing a rectangle for testing purposes
    #water_img_x = (x1+30,y1)
    #water_img_y = (w1-30,h1)
    #water_img = cv2.rectangle(img , water_img_x, water_img_y, (255, 0, 0), 3)

    #crop the image so that we do not detect the vertical lines of the cup
    #grab the height of the image for later use
    crop_img = img[y1:h1, x1+30:w1-30]
    height, width = crop_img.shape[:2]

    #cv2.imshow("cropped", crop_img)
    #cv2.waitKey(0)

    #gray scale and blur 
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray,(7,7),0)

    #changing the picture to strictly black and white to see the liquid
    (T, threshInv) = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)

    #get rid of the vertical lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (w1,1))
    horizontal_mask = cv2.morphologyEx(threshInv, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)

    #using canny, we draw out just the horizontal lines 
    edges = cv2.Canny(horizontal_mask, 50, 80)
    img_copy = crop_img.copy()
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    number_of_contours = len(hierarchy[0])
    #print(number_of_contours)

    #print(contours[number_of_contours-3])

    #draw out all of the horizontal lines 
    cv2.drawContours(img_copy, contours, -1, (0, 255, 0), 2)
    #print(contours)
    cv2.imshow("contours",img_copy)

    #choose the third highest contour, may change if there is a better solution
    cropped_height = contours[number_of_contours-3][1][0][1]


    #applying transformation on the line 
    #so that it is plotted properly on the original image
    contour_height = y1 + contours[number_of_contours-3][1][0][1]
    contour_x2 = contours[number_of_contours-3][1][0][0] + x1 + 30
    contour_x1 = contours[number_of_contours-3][0][0][0] + x1 + 30
    #print(contour_height)
    #print(height)
    #print(contour_x1)
    #print(contour_x2)

    #draw the line of the water level on original image
    start_point = (contour_x1,contour_height)
    end_point = (contour_x2, contour_height)
    img = cv2.line(img, start_point, end_point, (0, 255, 0), 2)
    cv2.imshow("Water Level", img)
    cv2.waitKey(0)

    #compare height of the line to the height of the cup
    aspectRatio = (height - cropped_height)/ float(height)

    #print(aspectRatio)

    #if water level is below 50%, the cup is low, other wise it doesnt need refill
    if aspectRatio > 0.5:
        #cv2.rectangle(img_copy, (x1, y1), (x1 + w1, y1 +(h1-contour_height[1])), (0, 255, 0), 2)
        print("Full")
        cv2.putText(img, "Full", (x1 + 10, contour_height - 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    else:
        #cv2.rectangle(img_copy, (x1, y1), (x1 + w1, y1 + (y1-contour_height[1])), (0, 0, 255), 2)
        print("Need Refill")
        cv2.putText(img, "Low", (x1 + 10, contour_height - 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
    cv2.imshow("Decision", img)

    cv2.waitKey(0)
