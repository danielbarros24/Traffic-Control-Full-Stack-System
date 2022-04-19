from asyncio import tasks
from flask import Flask, request, jsonify
from flask_cors import CORS
from tinydb import TinyDB, Query

app = Flask(__name__)
Cors = CORS(app)

# Database
db = TinyDB('db.json')
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

@app.post("/dash")
def ChartData():
    response = {'status': 'success'} 

    dash_data = request.get_json()

    cam = dash_data.get('cam'),
    time = dash_data.get('time'),
    task = dash_data.get('task'),

    print("Responded!")

    return {
        "cam": cam,
        "time": time,
        "task": task,
    }
        
    