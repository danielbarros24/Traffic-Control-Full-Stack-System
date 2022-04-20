from asyncio import tasks
from flask import Flask, request, jsonify
from flask_cors import CORS
from tinydb import TinyDB, Query
from datetime import datetime
import time

app = Flask(__name__)
Cors = CORS(app)

# Database
db = TinyDB('mqtt/db.json')
query = Query()

CORS(app, resources={r'/*': {'origins':
 '*'}}, CORS_SUPPORTS_CREDENTIALS=True)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/db', methods=['GET'])
def load():
    return jsonify(db.search(query.Data.Count == 24))

@app.post("/data")
def submitData():  
    response_object = {'status': 'success'} 
    
    post_data = request.get_json()     
    username = post_data.get('username'),     
    password = post_data.get('password') 

    print(username) 
    print(password)     

    response_object['message'] = username, password

    return response_object

@app.post("/dashboard")
def chartData():
    response = {'status': 'success'} 

    dash_data = request.get_json()
    cam = dash_data.get('cam')
    time = dash_data.get('time')
    subtask = dash_data.get('subtask')

    print("Responded!")
    print(cam)
    print(time)
    print(subtask)

    return jsonify(db.search(query.Subtask == subtask))


@app.post("/time")
def recentTime():
    response = {'status': 'success'} 

    dash_data = request.get_json()

    minTime = dash_data.get('minTime')

    print("Responded!")
    print(minTime)

    return jsonify(db.search(query.UtcTime >= minTime))