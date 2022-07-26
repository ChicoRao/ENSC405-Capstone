from flask import Flask, render_template, request
from flask import Flask, jsonify, render_template
<<<<<<< HEAD
# from waterLevelDetectionBlob import run1
# from dirtyPlateDetection import run2
=======
from ipDetection import ipSearch
>>>>>>> 143d286 (fixed polling and multiple emit on server)
from freeOccupiedDetection import freeOccupied
from imageComparison import compare
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
import json

from flask import request
url='http://192.168.1.82/capture?_cb=1656024603205'

tableID = "e1"
SavedLayout = []
SavedPassword = []

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
    t1 = time.time()
    # waterqueue = []
    # bowlqueue = []
    # platequeue = []
    occupancyqueue = []
    comparisonqueue  = []
    decisionqueue=[]
    calibration_img = capture_photo()
    i = 0
    tempTest = [
        {'status': "Available" , 'colour': "green"},
        {'status': "Occupied" , 'colour': "blue"},
        {'status': "Need Cleaning" , 'colour': "red"}
    ]
    while True:
        img_resp1=urllib.request.urlopen(url1)
        imgnp1=np.array(bytearray(img_resp1.read()),dtype=np.uint8)
        img1 = cv2.imdecode(imgnp1,-1)
        img_resp2=urllib.request.urlopen(url2)
        imgnp2=np.array(bytearray(img_resp2.read()),dtype=np.uint8)
        img2 = cv2.imdecode(imgnp2,-1)
        if not img1.all() and not img2.all():
            occupancy1 = freeOccupied(img1)
            occupancy2 = freeOccupied(img2)
            occupancyqueue1.append(occupancy1)
            occupancyqueue2.append(occupancy2)
            comparison1 = compare(img1, "base_photo_1.png")
            comparison2 = compare(img2, "base_photo_2.png")
            comparisonqueue1.append(comparison1) 
            comparisonqueue2.append(comparison2)
            
            # water_level = run1(img)
            # waterqueue.append(water_level) 
            occupancy = freeOccupied(img)
            occupancyqueue.append(occupancy)
            comparison = compare(img)
            comparisonqueue.append(comparison)
            # bowlStatus  = run2(img)
            # bowlqueue.append(bowlStatus)
            # plateStatus = run3(img)
            # platequeue.append(plateStatus)

            if (time.time() > t0+5):
                people = max(set(occupancyqueue), key=occupancyqueue.count)
                # emit('update value', people, broadcast=True)
                decisionqueue.append(people)
                # print(people)
                # waterlevelavg = max(set(waterqueue), key=waterqueue.count)
                # # emit('update value', waterlevelavg, broadcast=True)
                # decisionqueue.append(waterlevelavg)
                # # print(waterlevelavg)
                # bowl_stat = max(set(bowlqueue), key=bowlqueue.count)
                # decisionqueue.append(bowl_stat)
                # # print(bowl_stat)
                compare_stat = max(set(comparisonqueue), key=comparisonqueue.count)
                decisionqueue.append(compare_stat)

                # plate_stat = max(set(platequeue), key=platequeue.count)
                # decisionqueue.append(plate_stat)
                # print(plate_stat)


                occupancyqueue.clear()
                comparisonqueue.clear()
                # waterqueue.clear()
                # bowlqueue.clear()
                # platequeue.clear()
                t0 = time.time()
                if len(decisionqueue1) == 2 or len(decisionqueue2) == 2:
                    print("camera1 ", decisionqueue1)
                    print("camera2 ", decisionqueue2)
                    decision_status1 = decision(decisionqueue1)
                    decision_status2 = decision(decisionqueue2)
                    objectcolours1 = colours(decision_status1, tableID1)
                    objectcolours2 = colours(decision_status2, tableID2)
                    sendingDict[tableID1] = objectcolours1
                    sendingDict[tableID2] = objectcolours2
                    emit('update value', sendingDict)
                    decisionqueue1.clear()
                    decisionqueue2.clear()
                    sendingDict.clear()



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

@app.route("/SavePassword", methods = ['POST'])
def SavePassword():
    global SavedPassword
    SavedPassword = request.data
    # print(SavedLayout)
    print(request.data)
    f = open("password.txt", "w")
    f.write(request.data.decode("UTF-8"))
    f.close()
    return{"message": "Received Layout successfully"}


@app.route("/GetLayout", methods = ['GET'])
def GetLayout():
    return SavedLayout


if __name__ == "__main__":
    socketio.run(app, debug=True)
