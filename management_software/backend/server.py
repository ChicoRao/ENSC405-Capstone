from flask import Flask, render_template, request
from flask import Flask, jsonify, render_template
from ipDetection import ipSearch
from freeOccupiedDetection import freeOccupied
from imageComparison import compare
from handGesture import fourImages
from colours import colours
from decision import decision
from flask_socketio import SocketIO, emit
from random import random
from time import sleep
from flask_cors import CORS
import cv2
import urllib.request
import numpy as np
import time
from flask import request
import subprocess
# import _thread
import threading 
import queue
# from QR_calibration import read_qr_code
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from QR_calibration import return_QR_Result
from motion_detection import motion_detector

lock = threading.Lock()
urlList = ipSearch()
SavedLayout = []
# frame_count = 0



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode="threading" ,cors_allowed_origins="*")
cors = CORS(app)

@app.route("/capture", methods = ["PUT"])
def capture_photo():
    print("Capturing")
    for i in range(len(urlList)):
        converted_num = str(i)
        tableNumber = 'e'+ converted_num
        url = urlList[i]
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img = cv2.imdecode(imgnp,-1)
        img_name = "base_photo_"+ tableNumber + ".png"
        cv2.imwrite(img_name, img)
    return("captured")



def Gestures(frame, tableNumber):
    sendingAction = dict()
    gesture = fourImages(frame)
    result = return_QR_Result(frame)
    print(result)
    if result:
        
        if 'Water' in result:
            print ('QR is Water')
            sendingAction[tableNumber] = 'requests for Water (QR)'
            return sendingAction
        elif 'Bill' in result:
            print ('QR is Bill')
            sendingAction[tableNumber] = 'requests for Bill (QR)'
            return sendingAction
        elif 'Order' in result:
            print ('QR is Order')
            sendingAction[tableNumber] = 'requests for Order (QR)'
            return sendingAction
 
    if gesture:
        # print("GESTURE", gesture)
        if 'OK' in gesture :
            # sendingAction.append(tableNumber)
            # sendingAction.append('Bill')
            sendingAction[tableNumber] = 'requests for bill'
            return sendingAction

        elif 'Call' in gesture:
            # sendingAction.append(tableNumber)
            # sendingAction.append('Order')
            sendingAction[tableNumber] = 'requests to order'
            return sendingAction

        elif 'Peace' in gesture:
            # sendingAction.append(tableNumber)
            # sendingAction.append('Order')
            sendingAction[tableNumber] = 'requests for water refill'
            return sendingAction
        else:
            sendingAction[tableNumber] = 'Other'
            return sendingAction
            
def motion(previous_frame,prepared_frame,img_rgb):

    status = 'free'
    # 2. Calculate the difference

    # 3. Set previous frame and continue if there is None

    # calculate difference and update previous frame
    diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
    previous_frame = prepared_frame

    # 4. Dilute the image a bit to make differences more seeable; more suitable for contour detection
    kernel = np.ones((5, 5))

    diff_frame = cv2.dilate(diff_frame, kernel, 1)

    # 5. Only take different areas that are different enough (>20 / 255)
    thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[0]
    # 6. Find and optionally draw contours
    contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    # Comment below to stop drawing contours
    cv2.drawContours(image=img_rgb, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    if cv2.contourArea(contours) > 3:
        # too small: skip!
        print("motion deteced")
        status = 'Occupied'
    return status







def ChangeColours(previous_frame,prepared_frame,img,img_rgb, tableNumber):
    # frame_count= frame_count + 1
    decisionqueue = []
    sendingDict = dict()

    people = freeOccupied(img)
    people1 = motion(previous_frame,prepared_frame,img_rgb)

    decisionqueue.append(people)
    decisionqueue.append(people1)
    compare_stat = compare(img, "base_photo_"+ tableNumber +".png")
    decisionqueue.append(compare_stat)
    # decisionqueue.append(people1)

    decision_status = decision(decisionqueue)
    objectcolours = colours(decision_status, tableNumber)
    sendingDict[tableNumber] = objectcolours
    return sendingDict


def callingfunctions(q, q2, url, tableNumber):
    previous_frame = None
    prepared_frame = None

    # frame_count = 0
    while True:

        # print ('frame count is', frame_count)
        img_resp2=urllib.request.urlopen(url)
        imgnp2=np.array(bytearray(img_resp2.read()),dtype=np.uint8)
        frame = cv2.imdecode(imgnp2,-1) 

        img_brg = frame
        img_rgb = cv2.cvtColor(src=img_brg, code=cv2.COLOR_BGR2RGB)

    # 2. Prepare image; grayscale and blur

        prepared_frame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5, 5), sigmaX=0)
        prepared_frame = cv2.Canny(prepared_frame, 10, 90)

        if (previous_frame is None):
            print ('previous_frame is None')
  # First frame; there is no previous one yet
            previous_frame = prepared_frame
        
        checkQRtoRecalibrate(frame,tableNumber,url)
        # checkQR(frame,tableNumber)
        # FRAME = cv2.imdecode(imgnp2,-1) 
        # frame = rgb2gray(FRAME) 
        with lock:
            hands = Gestures(frame, tableNumber)
            q.put(hands)
            colour = ChangeColours(previous_frame,prepared_frame,frame,img_rgb, tableNumber)
            print('changing colors ran')
            q2.put(colour)    
            # QRcode = read_qr_code()
            # q3.put(QRcode)
            


def list_to_dict(ListOfDict):
    result = {}
    for d in ListOfDict:
        result.update(d)

    return result

def checkQRtoRecalibrate(img,tableNumber,url):
    result = return_QR_Result(img)
    print(result)
    if result:  
        if 'Calibration' in result:
            print ('QR is Calibration')
            time. sleep(7)
            img_resp3=urllib.request.urlopen(url)
            imgnp=np.array(bytearray(img_resp3.read()),dtype=np.uint8)
            img = cv2.imdecode(imgnp,-1)
            img_name = "base_photo_"+ tableNumber + ".png"
            cv2.imwrite(img_name, img)
            print('new base photo captured')
        return("new base photo captured")


@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Connected'})

@socketio.on('start stream')
def value_changed(message):
    capture_photo()
    q = queue.Queue()
    q2 = queue.Queue()
    # q3 = queue.Queue()
    for i in range(len(urlList)):
        with app.test_request_context():
            converted_num = str(i)
            tableNumber = 'e'+ converted_num
            print("Starting thread ", tableNumber , 'URl: ', urlList[i])
            thread = threading.Thread( target = callingfunctions, name = callingfunctions ,args = (q, q2, urlList[i], tableNumber), )
            thread.start()

    t0 = time.time()
    t1 = time.time()
    gestureList = []
    tableList = []
    # QRList = []
    while True:
        handGestures = q.get()
        tableColour = q2.get()
        # QR = q3.get()
        # print(tableColour)

        if handGestures != None:
            gestureList.append(handGestures)
        if tableColour != None:
            tableList.append(tableColour)
        # if QRList != None:
        #     QRList.append(QR)


        if time.time() >= t0 + 3:

            if gestureList and tableList:
                uniqueAction = []
                for x in gestureList:
                    if x not in uniqueAction:
                        uniqueAction.append(x)
                for action in uniqueAction:
                    if action.get(list(action.keys())[0]) == 'Other':
                        # emit("update value", { list(action.keys())[0] : "blue"})
                        print(tableList)
                        # if any((action.keys())[0] in d for d in tableList):
                        for value in tableList:
                            print(value)
                            print(list(action.keys())[0])
                            if (list(action.keys())[0] in value):
                                value.update({list(action.keys())[0]:"blue"})

                        gestureList.clear()
                        t0 =time.time()
                        # tableList.clear()
                        # tableList.append({ list(action.keys())[0] : "blue"})
                        continue
                    else:
                        emit('Action', action)
                        # emit("update value", { list(action.keys())[0] : "blue"})
                        print(tableList)
                        for value in tableList:
                            if (list(action.keys())[0] in value):
                                value.update({list(action.keys())[0]:"blue"})
                        # tableList.clear()
                        # tableList.append({ list(action.keys())[0] : "blue"})
                        gestureList.clear()
                        t0 =time.time()
                        continue
                
            if tableList and not gestureList:
                uniqueTableColour = []
                for x1 in tableList:
                    if x1 not in uniqueTableColour:
                        uniqueTableColour.append(x1)
                resultDict = list_to_dict(uniqueTableColour)

                if len(resultDict) >= len(urlList):
                    # print('HERE ', resultDict)
                    emit('update value', resultDict)
                    tableList.clear()
            t0 =time.time()


@app.route("/status")
def status():
    return{"status": "Available"}

@app.route("/message")
def message():

    return{"message": "Need Refill of Water"}


@app.route("/SaveLayout", methods = ['POST'])
def SaveLayout():
    global SavedLayout 
    SavedLayout = request.data
    print("recieved")
    return{"message": "Received Layout successfully"}


@app.route("/GetLayout", methods = ['GET'])
def GetLayout():
    if SavedLayout:
        return SavedLayout
    return {}


if __name__ == "__main__":
    socketio.run(app, debug=True)
