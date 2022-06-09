from flask import Flask, jsonify, redirect, url_for, session, flash
from flask import make_response, request, Response, render_template
from flask_login import LoginManager, login_required, login_user
from flask_session import Session
from flask_cors import CORS
from json_logic import jsonLogic

from tinydb import TinyDB, Query, where
from typing import Dict, Optional

from asyncio import tasks
from pickle import TRUE
from datetime import datetime

import attr
import os
import base64
import json
import random
import hashlib
import requests
import time
import re

app = Flask(__name__)

total_pins = 26

# DATABASE
db_camera = TinyDB('../database/camera.json')
db_auth = TinyDB('../database/auth.json')
db_processes = TinyDB('../database/processes.json')
db_system = TinyDB('../database/system.json')

query = Query()
Gpio = Query()

# CORS
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins':
 '*'}}, CORS_SUPPORTS_CREDENTIALS=True)
app.config['CORS_HEADERS'] = 'Content-Type'

# AUTH KEY
app.secret_key = '5e8a67084c7862b81e91f3dc1742335c'

#SESSION
login_manager = LoginManager()
login_manager.init_app(app)


@attr.s
class User(object):
    id = attr.ib()
    is_authenticated = True
    is_active = True
    is_anonymous = False

    def get_id(self):
        return self.id


users: Dict[str, User] = {}

@login_manager.user_loader
def load_user(user_id) -> Optional[User]:
    app.logger.debug('looking for user %s', user_id)
    u = users.get(user_id, None)
    if not id:
        return None
    return u


##### INDEX ######
@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'   
    return jsonify(access='ok')

##### If not logged - LOGIN #######
@app.route('/login', methods=['POST'])
def login():

    credentials = request.get_json() 
    username = credentials.get('username')
    password = credentials.get('password')

    if db_auth.search(query.username == username):
        username_el = db_auth.get(query.username == username)
        password_el = db_auth.get(query.password == password)
    
        if password_el:
            if username_el.doc_id == password_el.doc_id:
                            
                #next = flask.request.args.get('next')

                #if not is_safe_url(next):
                #    return flask.abort(400)
                print(username_el)
                return redirect(url_for('index'))
                
            return jsonify(status='Login unsuccessful! Please check your credentials.')
    return jsonify(status='Login unsuccessful! Please check your credentials.')        


#### LOGOUT #####
@app.route('/logout')
def logout():   
    session.pop('username', None)
    return redirect(url_for('index'))


############# OTHER FUNCTIONS ################

#####Create new automation########
@app.post('/process')
def new_process():
    automation = request.get_json()
    
    db_processes.insert(automation)
    
    print("Process inserted!")

    return jsonify(status='Success')


#####Update automation########
@app.patch('/process')
def update_process():

    automation = request.get_json()
    automation_id = request.args.get('id')

    if db_processes.contains(doc_id=int(automation_id)):    
        db_processes.update(automation, doc_ids=[int(automation_id)])
        res = "success"
        print("Process updated!")
    else:
        res = "not found" 

    return jsonify(status=res)

#####get automations########
@app.get('/process')
def get_process():
    
    automations = db_processes.all()

    for n in automations:
        n["id"] = n.doc_id

    print("Process returned!")    
    return jsonify(automations)

#####delete automations########
@app.delete('/process')
def delete_process():

    automation_id = request.args.get('id')
    if db_processes.contains(doc_id=int(automation_id)):   
        db_processes.remove(doc_ids=[int(automation_id)])
        res = "success"
        print("Process deleted!")
    else:
        res = "not found" 

    return jsonify(status=res)


#####get used GPIOs########
@app.get('/pins')
def get_pins():

    docs = [query.get('gpios') for query in db_processes.all()]    #GETS USED GPIOS IN AUTOMATIONS

    docs = [item for sublist in docs for item in sublist]

    used_pins = []

    for doc in docs:
        used_pins.append(doc.get('gpio'))

    Total_pins = list(range(1, 27))                                                         #CREATES ARRAY WITH ALL PINS (1 - 26)

    for j in used_pins:                                                                    #REMOVES FROM ARRAY USED GPIOS
       Total_pins.remove(j)

    return jsonify(Total_pins)

######## UPDATE PASSWORD #################################
@app.patch('/settings')
def update_password():

    credentials = request.get_json()
    password = credentials.get('password')

    db_auth.update({'password': "{}".format(password)})
    res = "success"
    print("Password updated!") 

    return jsonify(status=res)

######## GET BROKER MQTT #################################
@app.get('/settings-broker')
def get_broker():

    doc = db_system.get(doc_id=1)
    broker = doc.get('Broker_IP')
    print("[GET BROKER]: " + str(broker))

    return jsonify(Broker=broker)

######## GET SENSORS #################################
@app.get('/settings-sensors')
def get_sensors():

    doc = db_system.get(doc_id=1)
    
    number = doc.get('Sensors')
    print("[GET SENSORS]: " + str(number))

    return jsonify(Number=number)

######## UPDATE BROKER #################################
@app.patch('/settings-broker')
def update_broker():

    new_broker = request.get_json()
    broker = new_broker.get('Broker_IP')

    db_system.update({'Broker_IP': "{}".format(broker)})
    res = "success"
    print("Broker updated: " + str(broker)) 

    return jsonify(status=res)

######## UPDATE SENSORS #################################
@app.patch('/settings-sensors')
def update_sensors():

    new_sensors = request.get_json()

    db_system.update(new_sensors)

    res = "success"
    print("Sensors number updated: " + str(new_sensors)) 

    return jsonify(status=res)

######## GET ZONES #################################
@app.get('/settings-zones')
def get_zones():

    doc = db_system.get(doc_id=1)
    
    zones = doc.get('Zones')
    print("[GET ZONES]: " + str(zones))

    return jsonify(Zones=zones)


@app.post("/dashboard")
def chartData():

    dash_data = request.get_json()
    cam = dash_data.get('cam')
    time = dash_data.get('time')
    subtask = dash_data.get('subtask')

    print("Responded!") 
    print(cam)
    print(time)
    print(subtask)

    return jsonify(db_camera.search(query.Subtask == subtask))

def recentTime():

    dash_data = request.get_json()

    minTime = dash_data.get('minTime')

    print("Responded!")
    print(minTime)

    return jsonify(db_camera.search(query.UtcTime >= minTime))