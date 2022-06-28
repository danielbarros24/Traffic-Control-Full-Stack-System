
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager
from tinydb import TinyDB, Query
from datetime import timedelta
from filelock import Timeout, FileLock
import logging

app = Flask(__name__)

#disable logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

file_path = "src/backend/database/camera.json"
lock_path = "src/backend/database/camera.json.lock"
lock = FileLock(lock_path, timeout=20)

file_path_processes = "src/backend/database/processes.json"
lock_path_processes = "src/backend/database/processes.json.lock"
lock_processes = FileLock(lock_path, timeout=20)

file_path_system = "src/backend/database/system.json"
lock_path_system = "src/backend/database/system.json.lock"
lock_system = FileLock(lock_path, timeout=20)

jwt = JWTManager(app)
# DATABASE
db_auth = TinyDB('src/backend/database/auth.json')
db_system = TinyDB('src/backend/database/system.json')
db_sensors = TinyDB('src/backend/database/sensors.json')

query = Query()
Gpio = Query()

# CORS
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins':
                             '*'}}, CORS_SUPPORTS_CREDENTIALS=True)
app.config['CORS_HEADERS'] = 'Content-Type'

# AUTH KEY
app.config['JWT_SECRET_KEY'] = '5e8a67084c7862b81e91f3dc1742335c'

@app.route('/verify-token', methods=['POST'])
@jwt_required()
def verify_token():
    return jsonify({'success': True}), 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.post('/login')
def login():
    
    credentials = request.get_json()
    username = credentials.get('username')
    password = credentials.get('password')

    for doc in db_auth.all():
        if doc.get('username') == username:
            if check_password_hash(doc.get('password'), password):

                access_token = create_access_token(username, expires_delta= timedelta(hours=24))
                return jsonify({'success':True, 'token': access_token}), 200
            else:
                return jsonify(access='denied')
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401


##################################### SYSTEM FUNCTIONS ########################################################

##### CREATE NEW PROCESS ########################################################

@app.post('/process')
@jwt_required()
def new_process():
    with lock_processes:
        db_processes = TinyDB('src/backend/database/processes.json')
        
        automation = request.get_json()
        db_processes.insert(automation)

        #print("Process inserted!")

    return jsonify(status='ok')


##### UPDATE PROCESS ################################################################

@app.patch('/process')
@jwt_required()
def update_process():

    with lock_processes:
        db_processes = TinyDB('src/backend/database/processes.json')

        process = request.get_json()
        process_id = request.args.get('id')

        if db_processes.contains(doc_id=int(process_id)):
            db_processes.update(process, doc_ids=[int(process_id)])
            res = "success"
            #print("Process updated! id: " + str(process_id))
        else:
            res = "not found"

    return jsonify(status=res)


##### GET PROCESSE ################################################################

@app.get('/process')
@jwt_required()
def get_process():

    with lock_processes:
        db_processes = TinyDB('src/backend/database/processes.json')

        processes = db_processes.all()

        for n in processes:
            n["id"] = n.doc_id

        new_processes = processes

        for new_process in new_processes:
            id = new_process.doc_id
            if(new_process.get('notification') == True):
                db_processes.update({"notification": False}, doc_ids=[int(id)])

        #print("[GET PROCESSES]: Process returned!")

    return jsonify(processes)


##### DELETE PROCESSE ################################################

@app.delete('/process')
@jwt_required()
def delete_process():

    with lock_processes:
        db_processes = TinyDB('src/backend/database/processes.json')

        process_id = request.args.get('id')
        if db_processes.contains(doc_id=int(process_id)):
            db_processes.remove(doc_ids=[int(process_id)])
            res = "success"
            #print("Process deleted!" + str(process_id))
        else:
            res = "not found"

    return jsonify(status=res)


##### GET AVAILABLE GPIOs ########################################################

@app.get('/pins')
@jwt_required()
def get_pins():

    # GETS USED GPIOS IN AUTOMATIONS
    with lock_processes:
        db_processes = TinyDB('src/backend/database/processes.json')

        docs = [query.get('gpios') for query in db_processes.all()]

        docs = [item for sublist in docs for item in sublist]

    used_pins = []

    for doc in docs:
        used_pins.append(doc.get('gpio'))

    Total_pins = [4 ,5 ,6 ,7 ,8 ,9 ,10 ,11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]  # CREATES ARRAY WITH ALL AVAILABLE PINS 

    for j in used_pins:
        if j in Total_pins:  # REMOVES FROM ARRAY USED GPIOS
            Total_pins.remove(j)

    #print("[GET PINS]: " + str(Total_pins) + " Pins returned!")
    return jsonify(Total_pins)


######## UPDATE PASSWORD #########################################

@app.patch('/settings')
@jwt_required()
def update_password():

    credentials = request.get_json()
    password = credentials.get('password')

    hash_password = generate_password_hash(password)

    db_auth.update({'password': "{}".format(hash_password)})
    res = "ok"
    #print("Password updated!")

    return jsonify(status=res)


######## GET BROKER COMMUNICATION STATE  #################################################

@app.get('/broker-state')
@jwt_required()
def get_broker_communication():

    with lock_system:

        db_system = TinyDB('src/backend/database/system.json')
        doc = db_system.get(doc_id=1)
    state = doc.get('mqtt_connection')

    #print("[GET BROKER]: " + str(state))

    return jsonify(state=state)


######## GET MQTT BROKER IP ###############################################################

@app.get('/settings-broker')
@jwt_required()
def get_broker():

    with lock_system:

        db_system = TinyDB('src/backend/database/system.json')
    doc = db_system.get(doc_id=1)
    broker = doc.get('Broker_IP')
    #print("[GET BROKER]: " + str(broker))

    return jsonify(Broker=broker)


######## UPDATE MQTT BROKER ######################################################################

@app.patch('/settings-broker')
@jwt_required()
def update_broker():

    
    new_broker = request.get_json()
    broker = new_broker.get('Broker_IP')

    with lock_system:

        db_system = TinyDB('src/backend/database/system.json')
        db_system.update({'Broker_IP': "{}".format(broker)})
    res = "ok"
    #print("Broker updated: " + str(broker))

    return jsonify(status=res)


######## GET SENSORS #############################################################################

@app.get('/sensors')
@jwt_required()
def get_sensors():

    sensors = db_sensors.all()

    for n in sensors:
        n["id"] = n.doc_id

    #print("[GET SENSORS]: " + str(sensors))
    return jsonify(sensors)


######## INSERT SENSOR #############################################################################

@app.post('/sensors')
@jwt_required()
def create_sensors():

    sensor = request.get_json()

    db_sensors.insert(sensor)

    #print("Sensor inserted! Sensor " + str(sensor))
    res = "ok"
    return jsonify(status=res)


####### UPDATE SENSOR ###############################################################################

@app.patch('/sensors')
@jwt_required()
def update_sensor():

    sensor = request.get_json()
    sensor_id = request.args.get('id')

    if db_sensors.contains(doc_id=int(sensor_id)):
        db_sensors.update(sensor, doc_ids=[int(sensor_id)])
        res = "success"
        #print("Sensor updated! Sensor: " + str(sensor))
    else:
        res = "not found"

    return jsonify(status=res)


##### DELETE SENSOR ################################################

@app.delete('/sensors')
@jwt_required()
def delete_sensor():

    sensor_id = request.args.get('id')


    if db_sensors.contains(doc_id=int(sensor_id)):
        db_sensors.remove(doc_ids=[int(sensor_id)])
        res = "success"
        #print("Sensor deleted! id: " + str(sensor_id))
    else:
        res = "not found"

    return jsonify(status=res)

##### GET CHART DATA ################################################
@app.get('/chart')
@jwt_required()
def getChartData():

    with lock:
        db_camera = TinyDB('src/backend/database/camera.json')
    
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

    #print("[GET CHART DATA] Id: " + str(process_indicator))
    return jsonify(data)
