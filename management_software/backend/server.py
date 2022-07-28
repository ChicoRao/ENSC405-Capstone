from flask import Flask, render_template, request
from flask import Flask, jsonify, render_template
from ipDetection import ipSearch
from freeOccupiedDetection import freeOccupied
from imageComparison import compare
from handGesture import handGesture
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

urlList = ipSearch()

tableID1 = "e1"
tableID2 = "e2"
SavedLayout = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)

# app.register_blueprint(water)

@app.route("/capture")
def capture_photo():
    url1 = urlList[0]
    url2 = urlList[1]
    img_resp1=urllib.request.urlopen(url1)
    img_resp2=urllib.request.urlopen(url2)
    imgnp1=np.array(bytearray(img_resp1.read()),dtype=np.uint8)
    imgnp2=np.array(bytearray(img_resp2.read()),dtype=np.uint8)
    img1 = cv2.imdecode(imgnp1,-1)
    img2 = cv2.imdecode(imgnp2,-1)
    img_name1 = "base_photo_1.png"
    img_name2 = "base_photo_2.png"
    cv2.imwrite(img_name1, img1)
    cv2.imwrite(img_name2, img2)

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Connected'})

@socketio.on('start stream')
def value_changed(message):
    t0 = time.time()
    occupancyqueue1 = []
    comparisonqueue1  = []
    decisionqueue1=[]
    occupancyqueue2 = []
    comparisonqueue2  = []
    decisionqueue2=[]
    sendingDict = dict()
    # capture_photo()

    # url1 = urlList[0]
    # url2 = urlList[1]

    cap = cv2.VideoCapture(1)
    print("Starting Hand Gesture Detection")

    while True:
        _, frame = cap.read()
        
        handGestures = handGesture(frame)

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
