from flask import Flask, send_file
from sosfish_status import Status
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


@app.route("/fonts/uni_sans_thin.otf")
def discord_font():
    return send_file(f"{dir_path}/web/uni_sans_thin.otf")


@app.route("/fishinfo/<name>")
def fishinfo(name):
    user_data = loadUserData()
    output = Status(name, user_data)
    inventory = output.replace("\n","<br>")
    output = """<html><head>
    <style>
      @font-face { font-family: uni_sans_thin; src: url('/fonts/uni_sans_thin.otf'); } 
      h1 {
         font-family: uni_sans_thin
      }
      body {background-color: rgb(54,57,63);}
      h1 {color: white;}
    </style>
   </head>"""
    output = f"{output}<body><h1>{inventory}</h1></body></html>"
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
