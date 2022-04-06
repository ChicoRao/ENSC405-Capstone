from flask import Flask, render_template
from waterRefillDetection import somefunction
from flask_socketio import SocketIO, emit
from random import random
from time import sleep
from flask_cors import CORS

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
def value_changed(message):
    while True:
        # values[message['who']] = message['data']
        sleep(2)
        message = randomString()
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
    somefunction()
    return{"message": "Need Refill of Water"}

if __name__ == "__main__":
    socketio.run(app, debug=True)