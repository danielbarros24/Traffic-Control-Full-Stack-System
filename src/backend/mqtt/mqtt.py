# ------------------------------------------
# ---Only to test a simple system-----------
# ------------------------------------------
import json
import paho.mqtt.client as mqtt
from tinydb import TinyDB, Query
from filelock import Timeout, FileLock

db_sensors = TinyDB('src/backend/database/sensors.json')

query = Query()

file_path = "src/backend/database/camera.json"
lock_path = "src/backend/database/camera.json.lock"
lock = FileLock(lock_path, timeout=20)

# Server Credentials
username = "service"
password = "service#4123"

MQTT_Topics = []   
zones = []
sensors_list = []
vehicles_list = ["Car", "Bike", "Truck"]

n_sensors = len(db_sensors)
docs = db_sensors.all()

for doc in docs:
    sensor = doc.get('name')
    MQTT_Topics.append(sensor + "/onvif-ej/#")
    sensors_list.append(sensor)

flag_connected = 1
db_acess = 1            # if db_acess = 0 --> camera.json is being used!!

def set_flag():
    return flag_connected

def set_db_acess():
    return db_acess

def mqtt_data_received(msg):
    parse_mqtt_message(msg.topic, msg.payload)


def input_json_db(json_message):
    json_message_serialized = json.dumps(json_message)
    #print("[DATABASE INPUT]: " + str(json_message_serialized))
    print("[SUBSCRIBER]: MQTT DATA RECEIVED")
    with lock:
        db_camera = TinyDB('src/backend/database/camera.json')
        db_camera.insert(json.loads(json_message_serialized))


    #print("==========================DATA INSERTED IN DATABASE==========================" + "\n\n\n")


def create_RuleEngine_message(cam, utc_time, task, vehicle, zone, count):
    json_message = {
        "Cam": cam,
        "UtcTime": utc_time,
        "Task": task,
        "Vehicle": vehicle,
        "Zone": zone,
        "Count": count,
    }
    return json_message


def create_IVA_message(cam, utc_time, task, vehicle, zone, state):
    json_message = {
        "Cam": cam,
        "UtcTime": utc_time,
        "Task": task,
        "Vehicle": vehicle,
        "Zone": zone,
        "State": state,
    }
    return json_message


def create_noZone_message(cam, utc_time, task, vehicle, state):
    json_message = {
        "Cam": cam,
        "UtcTime": utc_time,
        "Task": task,
        "Vehicle": vehicle,
        "State": state,
    }
    return json_message


def create_noVehicle_message(cam, utc_time, task, zone, state):
    json_message = {
        "Cam": cam,
        "UtcTime": utc_time,
        "Task": task,
        "Zone": zone,
        "State": state,
    }
    return json_message


def parse_mqtt_message(topic, message):

    Topic_array = []
    Topic_array = topic.split("/")
    msg_deserialized = json.loads(message)

    _cam = Topic_array[0]
    _utc_time = msg_deserialized['UtcTime']

    if _cam in sensors_list:
        if Topic_array[2] == 'RuleEngine':
            if Topic_array[4] == 'Counter':
                rule = msg_deserialized['Source']['Rule']
                rule_split = rule.split()

                if len(rule_split) == 3 and rule_split[1] in vehicles_list:
                    _task = 'Counter'
                    _vehicle = rule_split[1]
                    _zone = _cam + '-' + rule_split[2]
                    _count = msg_deserialized['Data']['Count']

                    json_message = create_RuleEngine_message(_cam, _utc_time, _task, _vehicle, _zone, _count)
                    input_json_db(json_message)   
        elif Topic_array[2] == 'IVA':
            name = Topic_array[5]
            name_split = name.split()

            if len(name_split) == 2 and name_split[0] == 'Jam':
                    _task = 'Jam Detection'
                    _zone = _cam + '-' + name_split[1]
                    _state = msg_deserialized['Data']['State']

                    json_message = create_noVehicle_message(_cam, _utc_time, _task, _zone, _state)
                    input_json_db(json_message)

            elif Topic_array[3] == 'CrowdDetection':
                
                if Topic_array[5].find('Crowd') != -1 and Topic_array[5].find('Detection') != -1:
                    _task = 'Crowd Detection'
                    _zone = _cam
                    _state = msg_deserialized['Data']['State']

                    json_message = create_noVehicle_message(_cam, _utc_time, _task, _zone, _state)
                    input_json_db(json_message)

            elif Topic_array[3] == 'IdleObject' :
                _state = msg_deserialized['Data']['State']

                if len(name_split) == 3:

                    if name_split[0] == 'Idle':
                        _task = 'Idle Object'
                    elif name_split[0] == 'DoublePark':
                        _task = 'Double Park'
                    
                    if name_split[1] in vehicles_list: 
                        _vehicle = name_split[1]
                        _zone = _cam + '-' + name_split[2]

                        json_message = create_IVA_message(_cam, _utc_time, _task, _vehicle, _zone, _state)
                        input_json_db(json_message)
    

def on_connect(client, userdata, flags, rc):
    global flag_connected
    if rc == 0:
        for i in range(int(n_sensors)):
            client.subscribe(MQTT_Topics[i], 0)
        print("[MQTT]: Connection OK \n")
        flag_connected = 1
        return 0
    else:
        return "Connection Refused! Error code: " + str(rc)

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0
   print("[MQTT]: Connection DOWN \n")

def on_message(client, userdata, msg):

    topic_deserialized = msg.topic
    topic_array = topic_deserialized.split('/')

    if topic_array[2] == 'RuleEngine' or topic_array[2] == 'IVA':
        mqtt_data_received(msg)

def on_subscribe(client, userdata, mid, granted_qos):
    pass


client = mqtt.Client("mqtt-data-listener")

# Assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.username_pw_set(username, password)


