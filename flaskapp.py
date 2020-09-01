from flask import Flask
from fishstatus import Status
from flask import request
import os
import json
dir_path = os.path.dirname(os.path.realpath(__file__))
badge_names = ["Common People", "Uncommon Phenomonon", "A Rare Talent", "Absolute Legend", "Rod God"]

app = Flask(__name__)

def loadData(file):
    try:
        with open(f"{dir_path}/{file}.json", "r") as file:
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError:
                return {}
    except:
        return {}

def loadUserData():
    dat = {}
    dir = f"{dir_path}/fishingdata/users"
    for filename in os.listdir(dir):
        with open(os.path.join(dir, filename), "r") as f:
            name = filename[:-5]
            dat[name] = loadData(f"fishingdata/users/{name}")
    return dat

user_data = loadUserData()

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Eat shit Chris.</h1>"

@app.route("/fishinfo")
def fishinfo():
    angler=request.form["a"]
    output = Status(angler,user_data,badge_names)
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0')
