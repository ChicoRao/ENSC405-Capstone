from tracemalloc import start
import cv2
import cvlib as cv
import numpy as np
import sys
from cvlib.object_detection import draw_bbox
import math
from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import cv2
import os

#reading image from file
#does not work with cup 1
#works with cup 2,3,4,5
#kind of works with cup 11

#img = cv2.imread(r'C:\Users\<username>\Desktop\ENSC405-Capstone\openCV\WaterLevel') #might need to change the path

#empty table photo which should take at the time first setup LocalHost
imageA = cv2.imread(r'C:\Users\Irene\Desktop\405 OpenCV\ENSC405-Capstone\openCV\Detection of empty plate\pic7_esp32cam.jpg') #might need to change the path
#photo for comparing to empty table photo
imageB = cv2.imread(r'C:\Users\Irene\Desktop\405 OpenCV\ENSC405-Capstone\openCV\Detection of empty plate\pic5_esp32cam.jpg') #might need to change the path

#detecting the objects in the image
bbox, label, conf = cv.detect_common_objects(imageA)
im1 = draw_bbox(imageA, bbox, label, conf)
bbox, label, conf = cv.detect_common_objects(imageB)
im2 = draw_bbox(imageB, bbox, label, conf)

cv2.imshow('detection',im1)
cv2.imshow('detection2',im2)

# convert the images to grayscale
grayA = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned

(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours
for c in cnts:
# compute the bounding box of the contour and then draw the
# bounding box on both input images to represent where the two
# images differ
    area = cv2.contourArea(c)
    if area < 3000:
        continue
    else:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

#area = cv2.contourArea(c)
# show the output images
cv2.imshow("Original", imageA)
cv2.imshow("Modified", imageB)
#cv2.imshow("Diff", diff)
#cv2.imshow("Thresh", thresh)

if score >= 0.98: #check if table is clean and available
    print("available")
elif label[0] == 'person' or label[1] == 'person': #check if detected human
    print("not available")   
else: #check if the table need to clean
    print("need to clean")


cv2.waitKey(0)