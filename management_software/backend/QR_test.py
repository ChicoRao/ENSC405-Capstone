# import glob
# import cv2
# import pandas as pd
# import pathlib

# img = cv2.imread('C:\\Users\\patrick\\Desktop\\ENSC405-Capstone\\management_software\\backend\\frame.jpg')
# detect = cv2.QRCodeDetector()
# value, points, straight_qrcode = detect.detectAndDecode(img)
# print(value)
# print(type(value))
import cv2

from pyzbar.pyzbar import decode
img = cv2.imread('Bill.png')
for barcode in decode (img):
    print (barcode.data.decode("utf-8"))
