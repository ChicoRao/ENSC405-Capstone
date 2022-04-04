from flask import Blueprint

water = Blueprint('water',__name__)

@water.route("/water")

def waterLevel():
    return "empty"

def somefunction():
    print("Test Message")