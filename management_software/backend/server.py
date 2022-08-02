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

lock = threading.Lock()
urlList = ipSearch()
SavedLayout = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode="threading" ,cors_allowed_origins="*")
cors = CORS(app)

@app.route("/capture")
def capture_photo():
    for i in range(len(urlList)):
        converted_num = str(i)
        tableNumber = 'e'+ converted_num
        url = urlList[i]
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img = cv2.imdecode(imgnp,-1)
        img_name = "base_photo_"+ tableNumber + ".png"
        cv2.imwrite(img_name, img)



def Gestures(frame, tableNumber):
    sendingAction = dict()
    gesture = fourImages(frame)
 
    if gesture:
        if 'rock' in gesture :
            # sendingAction.append(tableNumber)
            # sendingAction.append('Bill')
            sendingAction[tableNumber] = 'Bill'
            return sendingAction

        elif 'peace' in gesture:
            # sendingAction.append(tableNumber)
            # sendingAction.append('Order')
            sendingAction[tableNumber] = 'Order'
            return sendingAction

def ChangeColours(img, tableNumber):
    decisionqueue = []
    sendingDict = dict()
    people = freeOccupied(img)
    decisionqueue.append(people)
    compare_stat = compare(img, "base_photo_"+ tableNumber +".png")
    decisionqueue.append(compare_stat)

    decision_status = decision(decisionqueue)
    objectcolours = colours(decision_status, tableNumber)
    sendingDict[tableNumber] = objectcolours
    return sendingDict


def callingfunctions(q, q2, url, tableNumber):
    while True:
        img_resp2=urllib.request.urlopen(url)
        imgnp2=np.array(bytearray(img_resp2.read()),dtype=np.uint8)
        frame = cv2.imdecode(imgnp2,-1) 
        with lock:
            hands = Gestures(frame, tableNumber)
            q.put(hands)
            colour = ChangeColours(frame,tableNumber)
            q2.put(colour)    


def list_to_dict(ListOfDict):
    result = {}
    for d in ListOfDict:
        result.update(d)

    return result


@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Connected'})

@socketio.on('start stream')
def value_changed(message):
    capture_photo()
    q = queue.Queue()
    q2 = queue.Queue()
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
    while True:
        handGestures = q.get()
        tableColour = q2.get()
        print(tableColour)

        if handGestures != None:
            gestureList.append(handGestures)
        if tableColour != None:
            tableList.append(tableColour)


        if time.time() >= t0 + 3:
            if gestureList:
                uniqueAction = []
                for x in gestureList:
                    if x not in uniqueAction:
                        uniqueAction.append(x)
                for action in uniqueAction:
                    emit('Action', action)
                gestureList.clear()
            if tableList:
                uniqueTableColour = []
                for x1 in tableList:
                    if x1 not in uniqueTableColour:
                        uniqueTableColour.append(x1)
                resultDict = list_to_dict(uniqueTableColour)

                if len(resultDict) >= len(urlList):
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
    return SavedLayout


if __name__ == "__main__":
    socketio.run(app, debug=True)
