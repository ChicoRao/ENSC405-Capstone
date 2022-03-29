# import the necessary packages from skimage.metrics import structural_similarity as compare_ssim
from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import cv2
import os
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
# --First and --Sedond are the path of the two images
#ap.add_argument("-f", "--first", required=True, help="first input image")
#ap.add_argument("-s", "--second", required=True, help="second")
#args = vars(ap.parse_args())

# load the two input images
imageA = cv2.imread(r'C:\Users\Irene\Desktop\405 OpenCV\ENSC405-Capstone\openCV\Image comparison (Cleandirty table)\pic1.jpeg') #might need to change the path
imageB = cv2.imread(r'C:\Users\Irene\Desktop\405 OpenCV\ENSC405-Capstone\openCV\Image comparison (Cleandirty table)\pic4.jpeg') #might need to change the path

# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned

(score, diff) = compare_ssim(grayA, grayB, gaussian_weights=True, full=True, sigma=7)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

if score == 1.0:
   print("clean") 
else:
    print("not clean")

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

    area = cv2.contourArea(c)
    # show the output images
    cv2.imshow("Original", imageA)
    cv2.imshow("Modified", imageB)
    #cv2.imshow("Diff", diff)
    #cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)
