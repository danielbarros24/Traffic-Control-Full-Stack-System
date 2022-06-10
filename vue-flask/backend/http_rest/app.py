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
db_sensors =TinyDB('../database/sensors.json')

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

    return jsonify(status='ok')


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

#####GET PROCESSES########
@app.get('/process')
def get_process():
    
    processes = db_processes.all()
    
    for n in processes:
        n["id"] = n.doc_id

    print("Process returned!")    

    new_processes = db_processes.all()

    for process in new_processes:
        process.update({"notification": False})
        db_processes.update(process)

    return jsonify(processes)

#####DELETE PROCESSES########
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


#####GET AVAILABLE GPIOs########
@app.get('/pins')
def get_pins():

    docs = [query.get('gpios') for query in db_processes.all()]    #GETS USED GPIOS IN AUTOMATIONS

    print(docs)
    docs = [item for sublist in docs for item in sublist]
    print("---------------------------------------------------------------------------------------------")
    print(docs)
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
    res = "ok"
    print("Password updated!") 

    return jsonify(status=res)

######## GET BROKER MQTT #################################
@app.get('/settings-broker')
def get_broker():

    doc = db_system.get(doc_id=1)
    broker = doc.get('Broker_IP')
    print("[GET BROKER]: " + str(broker))

    return jsonify(Broker=broker)


######## UPDATE BROKER #################################
@app.patch('/settings-broker')
def update_broker():

    new_broker = request.get_json()
    broker = new_broker.get('Broker_IP')

    db_system.update({'Broker_IP': "{}".format(broker)})
    res = "ok"
    print("Broker updated: " + str(broker)) 

    return jsonify(status=res)

######## GET SENSORS #################################
@app.get('/sensors')
def get_sensors():
    
    sensors = db_sensors.all()

    for n in sensors:
        n["id"] = n.doc_id

    print("Process returned!")    
    return jsonify(sensors)


######## INSERT SENSORS #################################
@app.post('/sensors')
def create_sensors():

    sensor = request.get_json()

    db_sensors.insert(sensor)
    print(sensor)

    print("Process inserted!")
    res = "ok"
    return jsonify(status=res)

##### UPDATE  SENSOR ########
@app.patch('/sensors')
def update_sensor():

    sensor = request.get_json()
    sensor_id = request.args.get('id')
    print(sensor_id)

    if db_sensors.contains(doc_id=int(sensor_id)):    
        db_sensors.update(sensor, doc_ids=[int(sensor_id)])
        res = "success"
        print("Sensor updated!")
    else:
        res = "not found" 

    return jsonify(status=res)

##### DELETE SENSORS ########
@app.delete('/sensors')
def delete_sensor():

    sensor_id = request.args.get('id')
    print(sensor_id)

    if db_sensors.contains(doc_id=int(sensor_id)):   
        db_sensors.remove(doc_ids=[int(sensor_id)])
        res = "success"
        print("Sensor deleted!")
    else:
        res = "not found" 

    return jsonify(status=res)


##### UPDATE PROCESS NOTIFICATION########
@app.patch('/process-notification')
def update_process_notification():

    process = request.get_json()
    process_id = request.args.get('id')

    if db_processes.contains(doc_id=int(process_id)):    
        db_processes.update(process, doc_ids=[int(process_id)])
        res = "success"
        print("Process updated!")
    else:
        res = "not found" 

    return jsonify(status=res)





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
