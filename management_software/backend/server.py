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
import _thread

urlList = ipSearch()
SavedLayout = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)

# app.register_blueprint(water)

@app.route("/capture")
def capture_photo():
    # url1 = urlList[0]
    # url2 = urlList[1]
    # img_resp1=urllib.request.urlopen(url1)
    # img_resp2=urllib.request.urlopen(url2)
    # imgnp1=np.array(bytearray(img_resp1.read()),dtype=np.uint8)
    # imgnp2=np.array(bytearray(img_resp2.read()),dtype=np.uint8)
    # img1 = cv2.imdecode(imgnp1,-1)
    # img2 = cv2.imdecode(imgnp2,-1)
    # img_name1 = "base_photo_1.png"
    # img_name2 = "base_photo_2.png"
    # cv2.imwrite(img_name1, img1)
    # cv2.imwrite(img_name2, img2)

    for i in range(len(urlList)):
        converted_num = str(i)
        tableNumber = 'e'+ converted_num
        url = urlList[i]
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img = cv2.imdecode(imgnp,-1)
        img_name = "base_photo_"+ tableNumber + ".png"
        cv2.imwrite(img_name, img)



# def Gestures(frame, tableNumber):
#     gesture = fourImages(frame)
#     if gesture and time.time() > t0+3:
#         if 'rock' in gesture :
#             t0 = time.time()
#             sendingAction.append(tableNumber)
#             sendingAction.append('Bill')
#             print("Sending rock", sendingAction)
#             emit('Action', sendingAction)
#         elif 'peace' in gesture:
#             print("Sending peace",sendingAction)
#             t0 = time.time()
#             sendingAction.append(tableNumber)
#             sendingAction.append('Order')
#             emit('Action', sendingAction)
#         sendingAction.clear()

# def ChangeColours(img, tableNumber):
    
#     occupancy = freeOccupied(frame)
#     occupancyqueue.append(occupancy)
#     comparison = compare(frame, "base_photo_"+ converted_num +".png")
#     comparisonqueue.append(comparison) 
        
#         people = max(set(occupancyqueue), key=occupancyqueue.count)
#         decisionqueue.append(people)
#         compare_stat = max(set(comparisonqueue), key=comparisonqueue.count)
#         decisionqueue.append(compare_stat)
#         occupancyqueue.clear()
#         comparisonqueue.clear()
#         decision_status = decision(decisionqueue)
#         objectcolours = colours(decision_status, tableNumber)
#         sendingDict[tableNumber] = objectcolours
#         print(sendingDict)
#         emit('update value', sendingDict)
#         decisionqueue.clear()

# def callingfunctions(url, tableNumber):
#     while True:
#         img_resp2=urllib.request.urlopen(url)
#         imgnp2=np.array(bytearray(img_resp2.read()),dtype=np.uint8)
#         frame = cv2.imdecode(imgnp2,-1) 
#         t0 = time.time()
#         t1 = time.time()
#         Gestures(frame, tableNumber)
#         ChangeColours(frame,tableNumber)
        


@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Connected'})

@socketio.on('start stream')
def value_changed(message):


    # capture_photo()

    # try:
    #     for i in range(len(urlList)):
    #         converted_num = str(i)
    #         tableNumber = 'e'+ converted_num
    #         thread.start_new_thread( callingfunctions, (url, tableNumber, ) )

    # except:
    #     print "Error: unable to start thread"

    # while 1:
    #     pass

    t0 = time.time()
    t1 = time.time()
    occupancyqueue = []
    comparisonqueue  = []
    decisionqueue=[]
    sendingDict = dict()
    sendingAction=[]
    capture_photo()
    

    print("Starting Hand Gesture Detection")

    while True:
        # _, frame = cap.read()
        for i in range(len(urlList)):
            img_resp2=urllib.request.urlopen(urlList[i])
            imgnp2=np.array(bytearray(img_resp2.read()),dtype=np.uint8)
            frame = cv2.imdecode(imgnp2,-1) 
            converted_num = str(i)
            tableNumber = 'e'+ converted_num
            print(tableNumber)
            if not frame.all():
                #hand gestures
                gesture = fourImages(frame)
                if gesture and time.time() > t0+3:
                    if 'rock' in gesture :
                        t0 = time.time()
                        sendingAction.append(tableNumber)
                        sendingAction.append('Bill')
                        print("Sending rock", sendingAction)
                        emit('Action', sendingAction)
                    elif 'peace' in gesture:
                        print("Sending peace",sendingAction)
                        t0 = time.time()
                        sendingAction.append(tableNumber)
                        sendingAction.append('Order')
                        emit('Action', sendingAction)
                    sendingAction.clear()
                #colour stuff
                occupancy = freeOccupied(frame)
                occupancyqueue.append(occupancy)
                comparison = compare(frame, "base_photo_"+ tableNumber +".png")
                comparisonqueue.append(comparison) 
                if (time.time() > t1+3):
                    people = max(set(occupancyqueue), key=occupancyqueue.count)
                    decisionqueue.append(people)
                    compare_stat = max(set(comparisonqueue), key=comparisonqueue.count)
                    decisionqueue.append(compare_stat)
                    occupancyqueue.clear()
                    comparisonqueue.clear()
                    
                    # if len(decisionqueue) == 2:
                    decision_status = decision(decisionqueue)
                    objectcolours = colours(decision_status, tableNumber)
                    sendingDict[tableNumber] = objectcolours
                    print(sendingDict)
                    # emit('update value', sendingDict)
                    decisionqueue.clear()

        if len(sendingDict) == len(urlList):
            print("sending colours", sendingDict)
            emit('update value', sendingDict)
            sendingDict.clear()
            t1 = time.time()

        # img_resp1=urllib.request.urlopen(url1)
        # imgnp1=np.array(bytearray(img_resp1.read()),dtype=np.uint8)
        # img1 = cv2.imdecode(imgnp1,-1)
        # img_resp2=urllib.request.urlopen(url2)
        # imgnp2=np.array(bytearray(img_resp2.read()),dtype=np.uint8)
        # img2 = cv2.imdecode(imgnp2,-1)
        # if not img1.all() and not img2.all():
        #     occupancy1 = freeOccupied(img1)
        #     occupancy2 = freeOccupied(img2)
        #     occupancyqueue1.append(occupancy1)
        #     occupancyqueue2.append(occupancy2)
        #     comparison1 = compare(img1, "base_photo_1.png")
        #     comparison2 = compare(img2, "base_photo_2.png")
        #     comparisonqueue1.append(comparison1) 
        #     comparisonqueue2.append(comparison2)



        #     if (time.time() > t0+5):
        #         people1 = max(set(occupancyqueue1), key=occupancyqueue1.count)
        #         people2 = max(set(occupancyqueue2), key=occupancyqueue2.count)
        #         decisionqueue1.append(people1)
        #         decisionqueue2.append(people2)
        #         compare_stat1 = max(set(comparisonqueue1), key=comparisonqueue1.count)
        #         compare_stat2 = max(set(comparisonqueue2), key=comparisonqueue2.count)
        #         decisionqueue1.append(compare_stat1)
        #         decisionqueue2.append(compare_stat2)
        #         occupancyqueue1.clear()
        #         comparisonqueue2.clear()
        #         occupancyqueue1.clear()
        #         comparisonqueue2.clear()
        #         t0 = time.time()
        #         if len(decisionqueue1) == 2 or len(decisionqueue2) == 2:
        #             print("camera1 ", decisionqueue1)
        #             print("camera2 ", decisionqueue2)
        #             decision_status1 = decision(decisionqueue1)
        #             decision_status2 = decision(decisionqueue2)
        #             objectcolours1 = colours(decision_status1, tableID1)
        #             objectcolours2 = colours(decision_status2, tableID2)
        #             sendingDict[tableID1] = objectcolours1
        #             sendingDict[tableID2] = objectcolours2
        #             emit('update value', sendingDict)
        #             decisionqueue1.clear()
        #             decisionqueue2.clear()
        #             sendingDict.clear()



def randomString():
    #infinite loop of magical random numbers
    number = round(random()*10, 3)
    return number


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
    return SavedLayout


if __name__ == "__main__":
    socketio.run(app, debug=True)
