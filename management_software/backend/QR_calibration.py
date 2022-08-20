import glob
import cv2
import pandas as pd
import pathlib



    

def read_qr_code(img):
    """Read an image and read the QR code.
    
    Args:
        filename (string): Path to file
    
    Returns:
        qr (string): Value from QR code
    """
    
    try:
        img = cv2.imread(img)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value   #if QR_LocalHost.png is on the table and scanned, this will return "http://LocalHost"
    except:
        return



