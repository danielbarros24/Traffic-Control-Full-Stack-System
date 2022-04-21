from asyncio import tasks
from flask import Flask, request, jsonify
from flask_cors import CORS
from tinydb import TinyDB, Query, where
from datetime import datetime
from flask_login import LoginManager, UserMixin
import time

app = Flask(__name__)
Cors = CORS(app)

# Database
db = TinyDB('mqtt/db.json')
db_auth = TinyDB('auth.json')

query = Query()

CORS(app, resources={r'/*': {'origins':
 '*'}}, CORS_SUPPORTS_CREDENTIALS=True)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '5e8a67084c7862b81e91f3dc1742335c'


@app.route('/login', methods=['POST'])
def login():

    credentials = request.get_json() 
    username = credentials.get('username')
    password = credentials.get('password')

    print(username)
    print(db_auth.search())
    print("check")

    if db_auth.search(query.username == username):
        return jsonify(status='ok')
    else:
        return jsonify(status='wrong')


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

    dash_data = request.get_json()
    cam = dash_data.get('cam')
    time = dash_data.get('time')
    subtask = dash_data.get('subtask')

    print("Responded!")
    print(cam)
    print(time)
    print(subtask)

    return jsonify(db.search(query.Subtask == subtask))

def recentTime():

    dash_data = request.get_json()

    minTime = dash_data.get('minTime')

    print("Responded!")
    print(minTime)

    return jsonify(db.search(query.UtcTime >= minTime))
