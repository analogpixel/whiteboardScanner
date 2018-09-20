#!/usr/bin/env python

import flask
from flask import Flask, jsonify, g, request, redirect, render_template

# pip install flask-cors
from flask_cors import CORS

import base64
import logging
import sys
import marker
import s3con
import json

app = Flask(__name__, static_url_path='/static' )
CORS(app)

@app.route('/')
def hello():
    return app.send_static_file('index.html')

@app.route('/showRoom/<roomName>')
def showRoom(roomName):
    return render_template('showRoom.html', roomName=roomName)

@app.route('/upload', methods=['POST'])
def uploadImage():
    print("got to the uploadImage")
    (header,data) = request.form.get('imgdata').split(',')
    roomName      = request.form.get('roomName', 'default')
    fileName      = "process_" + roomName + ".jpg"
    open("cache/" + fileName, "wb").write(base64.b64decode(data))
    m = marker.markerDetection("cache/" + fileName)
    s = s3con.s3Con()
    s.upload(m.exportFile, roomName)
    return "final file" + m.exportFile

@app.route('/listRoom/<roomName>')
def listRooms(roomName):
    s = s3con.s3Con()
    files = s.listFiles(roomName)
    return json.dumps(["{}".format(x['Key']) for x in files])
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port="9999", debug=True)
