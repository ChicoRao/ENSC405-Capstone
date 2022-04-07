from flask import Flask, render_template
from waterRefillDetection import run1
from freeOccupiedDetection import freeOccupied
from flask_socketio import SocketIO, emit
from random import random
from time import sleep
from flask_cors import CORS
import cv2
import urllib.request
import numpy as np
import time
url='http://10.0.0.102/capture?_cb=1649020515981'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
cors = CORS(app)

# app.register_blueprint(water)
values = {
    'slider1': 25,
    'slider2': 0,
}

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
    while True:
        # values[message['who']] = message['data']
        # sleep(2)
        # message = randomString()
        # emit('update value', message, broadcast=True)
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img = cv2.imdecode(imgnp,-1)
        
        
        water_level = run1(img)
        waterqueue.append(water_level)
        if (time.time() > t0+1):
            message = max(set(waterqueue), key=waterqueue.count)
            emit('update value', message, broadcast=True)
            waterqueue.clear()
            t0 = time.time()

        message = freeOccupied(img)
        emit('update value', message, broadcast=True)

            


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
