from flask import Flask
from fishstatus import Status
from flask import request
import os
import json
dir_path = os.path.dirname(os.path.realpath(__file__))
badge_names = ["Common People", "Uncommon Phenomonon", "A Rare Talent", "Absolute Legend", "Rod God"]

app = Flask(__name__)

def loadList(file, keepcaps = False):
    f = open(f"{dir_path}/fishingdata/{file}.txt", "r")
    data = [line.strip().lower() for line in f]
    f.close()
    return data
herbs = loadList("herbs")
spices = loadList("spices")


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

@app.route("/fishinfo/<name>")
def fishinfo(name):
    output = Status(name, user_data, herbs, spices, badge_names)
    output = output.replace("\n","<br>")
    output = f"<html><p>{output}</p></html>"
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0')
