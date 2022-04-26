from flask import Flask, jsonify, redirect, url_for, session, flash
from flask import make_response, request, Response, render_template
from flask_login import LoginManager, login_required, login_user
from flask_session import Session
from flask_cors import CORS

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

app = Flask(__name__)


# DATABASE
db = TinyDB('mqtt/db.json')
db_auth = TinyDB('auth.json')
query = Query()

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
    return jsonify(access='granted')

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

                return redirect(url_for('index'))
                
            return jsonify(status='Login unsuccessful! Please check your credentials.')
    return jsonify(status='Login unsuccessful! Please check your credentials.')        


#### LOGOUT #####
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))




############# OTHER FUNCTIONS ################

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
