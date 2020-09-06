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


@app.route("/fonts/default_text.otf")
def discord_font():
    return send_file(f"{dir_path}/web/Roboto-Light.ttf")

@app.route("/favicon.ico")
def favicon():
    return send_file(f"{dir_path}/web/favicon.ico")

@app.route("/fishinfo/<name>")
def fishinfo(name):
    user_data = loadUserData()
    output = Status(name, user_data)
    inventory = output.replace("\n","<br>")
    output = """<html><head>
    <style>
      @font-face { font-family: default_text; src: url('/fonts/default_text.otf'); } 
      h1 {
         font-weight: normal;
         font-family: default_text;
         font-size: 100%;
      }
      body {background-color: rgb(54,57,63);}
      h1 {color: white;}
    </style>
    <link rel="icon" 
      type="image/png" 
      href="http://mena.to/favicon.ico">
   </head>"""
    heart = "♥"
    inventory = inventory.replace(":heart:", heart)
    output = f"{output}<body><h1>{inventory}</h1></body></html>"
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
