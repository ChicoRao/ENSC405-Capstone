from flask import Flask
from waterRefillDetection import somefunction

app = Flask(__name__)

# app.register_blueprint(water)

@app.route("/status")
def status():
    return{"status": "Available"}

@app.route("/message")
def message():
    somefunction()
    return{"message": "Need Refill of Water"}

if __name__ == "__main__":
    app.run(debug=True)