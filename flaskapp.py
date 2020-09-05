from flask import Flask
from sosfish_status import Status
from sosfish_constants import herbs
from sosfish_constants import spices
from flask import request
import os
import json
dir_path = os.path.dirname(os.path.realpath(__file__))

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



@app.route("/")
def hello():
    return "<h1 style='color:blue'>Eat shit Chris.</h1>"

@app.route("/fishinfo/<name>")
def fishinfo(name):
    user_data = loadUserData()
    output = Status(name, user_data)
    output = output.replace("\n","<br>")
    output = f"<html><p>{output}</p></html>"
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
