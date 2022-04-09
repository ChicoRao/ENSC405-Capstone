from flask import Flask, render_template
from waterRefillDetection import run1
from freeOccupiedDetection import freeOccupied
from decision import decision
from flask_socketio import SocketIO, emit
from random import random
from time import sleep
from flask_cors import CORS
import cv2
import urllib.request
import numpy as np
import time
url='http://192.168.13.1/capture?_cb=1649362415215'


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
    print("{} written!".format(img_name))
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
    waterqueue = []
    occupancyqueue = []
    decisionqueue=[]
    # calibration_img = capture_photo()
    while True:
        emit('update button pressed', "Updated")
        # values[message['who']] = message['data']
        # sleep(2)
        # message = randomString()
        # emit('update value', message, broadcast=True)
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img = cv2.imdecode(imgnp,-1)
        
        water_level = run1(img)
        waterqueue.append(water_level)
        occupancy = freeOccupied(img)
        occupancyqueue.append(occupancy)
        if (time.time() > t0+1):
            people = max(set(occupancyqueue), key=occupancyqueue.count)
            # emit('update value', people, broadcast=True)
            decisionqueue.append(people)
            print(people)
            waterlevelavg = max(set(waterqueue), key=waterqueue.count)
            # emit('update value', waterlevelavg, broadcast=True)
            decisionqueue.append(waterlevelavg)
            print(waterlevelavg)
            occupancyqueue.clear()
            waterqueue.clear()
            t0 = time.time()
        if len(decisionqueue) == 2:
            decisionstatus = decision(decisionqueue)
            emit('update value', decisionstatus, broadcast=True)
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


if __name__ == "__main__":
    socketio.run(app, debug=True)
