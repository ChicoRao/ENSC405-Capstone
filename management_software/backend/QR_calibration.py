import glob
import cv2
import pandas as pd
import pathlib
from pyzbar.pyzbar import decode


    

def read_qr_code(img):
    """Read an image and read the QR code.
    
    Args:
        filename (string): Path to file
    
    Returns:
        qr (string): Value from QR code
    """
    

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # img = cv2.imread('frame.jpg')
    print ("qr image read")
    for barcode in decode (img):
        # print (barcode.data.decode("utf-8"))
        return barcode.data.decode("utf-8")   #if QR_LocalHost.png is on the table and scanned, this will return "http://LocalHost"
  
def return_QR_Result(img):
    ActionList = []
    ActionList.append(read_qr_code(img))
    return ActionList


