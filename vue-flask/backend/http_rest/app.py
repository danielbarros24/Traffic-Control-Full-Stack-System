
from flask import Flask, jsonify, redirect, url_for, session, flash
from flask import make_response, request, Response, render_template
from flask_login import LoginManager, login_required, login_user
from flask_session import Session
from flask_cors import CORS
from json_logic import jsonLogic
from werkzeug.security import generate_password_hash, check_password_hash
import json

import jwt

from functools import wraps

from tinydb import TinyDB, Query, where
from typing import Dict, Optional

from asyncio import tasks
from pickle import TRUE
from datetime import datetime, timedelta

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
db_sensors = TinyDB('../database/sensors.json')

query = Query()
Gpio = Query()

# CORS
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins':
                             '*'}}, CORS_SUPPORTS_CREDENTIALS=True)
app.config['CORS_HEADERS'] = 'Content-Type'

# AUTH KEY
app.config['SECRET-KEY'] = '5e8a67084c7862b81e91f3dc1742335c'


def token_required(f):
    @wraps(f)
    def decoreated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt(token, app.config['SECRET-KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decoreated


@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'Only who is authenticated can view this!'})


@app.post('/login')
def login():

    credentials = request.get_json()
    username = credentials.get('user')
    password = credentials.get('password')
    print(1111)
    for doc in db_auth.all():
        if doc.get('username') == username:
            if check_password_hash(doc.get('password'), password):

                token = jwt.encode({'sub': username, 'iat': datetime.utcnow(), 'exp': datetime.utcnow(
                ) + timedelta(minutes=30)}, app.config['SECRET-KEY'])
                return jsonify({'token': token})
            else:
                return jsonify(access='denied')
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

#### LOGOUT #####


@app.route('/logout')
def logout():
    session.pop('username', None)
    print("Logout!")
    print("Session closed!")
    return redirect(url_for('index'))


############# SYSTEM FUNCTIONS ################

#####CREATE NEW PROCESS########
@app.post('/process')
def new_process():
    automation = request.get_json()

    db_processes.insert(automation)

    print("Process inserted!")

    return jsonify(status='ok')

#####UPDATE PROCESS########


@app.patch('/process')
def update_process():

    process = request.get_json()
    process_id = request.args.get('id')

    if db_processes.contains(doc_id=int(process_id)):
        db_processes.update(process, doc_ids=[int(process_id)])
        res = "success"
        print("Process updated! id: " + str(process_id))
    else:
        res = "not found"

    return jsonify(status=res)

#####GET PROCESSES########


@app.get('/process')
def get_process():

    processes = db_processes.all()

    for n in processes:
        n["id"] = n.doc_id

    new_processes = processes

    for new_process in new_processes:
        id = new_process.doc_id
        if(new_process.get('notification') == True):
            db_processes.update({"notification": False}, doc_ids=[int(id)])

    print("[GET PROCESSES]: Process returned!")

    return jsonify(processes)

#####DELETE PROCESSES########


@app.delete('/process')
def delete_process():

    process_id = request.args.get('id')
    if db_processes.contains(doc_id=int(process_id)):
        db_processes.remove(doc_ids=[int(process_id)])
        res = "success"
        print("Process deleted!" + str(process_id))
    else:
        res = "not found"

    return jsonify(status=res)

#####GET AVAILABLE GPIOs########


@app.get('/pins')
def get_pins():

    # GETS USED GPIOS IN AUTOMATIONS
    docs = [query.get('gpios') for query in db_processes.all()]

    docs = [item for sublist in docs for item in sublist]

    used_pins = []

    for doc in docs:
        used_pins.append(doc.get('gpio'))

    Total_pins = list(range(1, 27))  # CREATES ARRAY WITH ALL PINS (1 - 26)

    for j in used_pins:
        if j in Total_pins:  # REMOVES FROM ARRAY USED GPIOS
            Total_pins.remove(j)

    print("[GET PINS]: " + str(Total_pins) + " Pins returned!")
    return jsonify(Total_pins)

######## UPDATE PASSWORD #################################


@app.patch('/settings')
def update_password():

    credentials = request.get_json()
    password = credentials.get('password')

    hash_password = generate_password_hash(password)

    db_auth.update({'password': "{}".format(hash_password)})
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

    print("[GET SENSORS]: " + str(sensors))
    return jsonify(sensors)

######## INSERT SENSORS #################################


@app.post('/sensors')
def create_sensors():

    sensor = request.get_json()

    db_sensors.insert(sensor)
    print(sensor)

    print("Sensor inserted! Sensor " + str(sensor))
    res = "ok"
    return jsonify(status=res)

##### UPDATE  SENSOR ########


@app.patch('/sensors')
def update_sensor():

    sensor = request.get_json()
    sensor_id = request.args.get('id')

    if db_sensors.contains(doc_id=int(sensor_id)):
        db_sensors.update(sensor, doc_ids=[int(sensor_id)])
        res = "success"
        print("Sensor updated! Sensor: " + str(sensor))
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
        print("Sensor deleted! id: " + str(sensor_id))
    else:
        res = "not found"

    return jsonify(status=res)


@app.get('/chart')
def getChartData():

    counter_list = ["1", "2", "3"]
    data = []

    process_sensor = request.args.get('sensor')
    process_startTime = request.args.get('startTime')
    process_endTime = request.args.get('endTime')
    process_indicator = request.args.get('indicator')

    vehicle = ''
    if process_indicator in counter_list:

        if process_indicator == "1":
            vehicle = 'Car'
        if process_indicator == "2":
            vehicle = 'Truck'
        if process_indicator == "3":
            vehicle = 'Bike'
        docs = db_camera.search((query.Task == 'Counter') & (
            query.Cam == process_sensor) & (query.Vehicle == vehicle) & (query.UtcTime > process_startTime) & (query.UtcTime < process_endTime))

        for doc in docs:
            msg = {"{}".format(doc.get('UtcTime')): doc.get('Count')}
            data.append(msg)

    if process_indicator == "4":  # COUNT DOUBLE-PARK
        docs = db_camera.search((query.Task == 'Double Park') & (
            query.Cam == process_sensor) & (query.UtcTime < process_endTime) & (query.State == "true"))
        n = 0
        for doc in docs:
            n += 1
            if doc.get('UtcTime') > process_startTime:
                msg = {"{}".format(doc.get('UtcTime')): n}
                data.append(msg)

    print("[GET CHART DATA] Id: " + str(process_indicator))
    return jsonify(data)
