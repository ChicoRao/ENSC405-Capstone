from flask import Flask, render_template, request
# from bowlStatusDetection import bowlStatus
# from plateStatusDetection import plateStatus
# from waterRefillDetection import run1
# from bowlStatusDetection import run2
# from plateStatusDetection import run3
from flask import Flask, jsonify, render_template
from ipDetection import ipSearch
# from waterLevelDetectionBlob import run1
# from dirtyPlateDetection import run2
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
from flask import request
import subprocess

url = ipSearch()

tableID = "e1"
SavedLayout = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)

# app.register_blueprint(water)
values = {
    'slider1': 25,
    'slider2': 0,
}

@app.route("/capture")
def capture_photo():
    img_resp=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgnp,-1)
    img_name = "base_photo_.png"
    cv2.imwrite(img_name, img)
    # print("{} written!".format(img_name))
    return img

@app.route("/")
def index():
    return render_template('index.html', **values)

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Connected'})

@socketio.on('Slider value changed')
def value_changed(message, ):
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
        # if (time.time() > t1+5):
        #     i = i%3
        #     emit('update value', tempTest[i], broadcast=True)
        #     t1 = time.time()
        #     i += 1
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img = cv2.imdecode(imgnp,-1)
        # print(img)
        if not img.all():
            
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
                if len(decisionqueue) == 2:
                    print(decisionqueue)
                    decision_status = decision(decisionqueue)

                    print(decision_status)
                    objectcolours = colours(decision_status, tableID)
                    print(objectcolours)
                    emit('update value', objectcolours, broadcast=True)
                    decisionqueue.clear()



def randomString():
    #infinite loop of magical random numbers
    number = round(random()*10, 3)
    return str(number)


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
    # print(SavedLayout)
    print("recieved")
    return{"message": "Received Layout successfully"}


@app.route("/GetLayout", methods = ['GET'])
def GetLayout():
    # print(SavedLayout)
    # print("sending")
    return SavedLayout
    # return{"message": "Received Layout successfully"}


if __name__ == "__main__":
    socketio.run(app, debug=True)