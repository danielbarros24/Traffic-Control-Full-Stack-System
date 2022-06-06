# ------------------------------------------
# ---Only to test a simple system-----------
# ------------------------------------------

import paho.mqtt.client as mqtt
from tinydb import TinyDB, Query

db_system = TinyDB('database/system.json')
db_camera = TinyDB('database/camera.json')

query = Query()

import json
# from store_data_into_db import sensor_Data_Handler
# from tiny_db_manager import Data_handler


docs = db_system.all()
for doc in docs:
    n_sensors = doc.get('Sensors')

print("Number of cameras: " + n_sensors)


# Server Credentials
username = "daniel"
password = "password"

#new_data = 0

MQTT_Topics = []   
zones = []
 
for i in range(int(n_sensors)):
    j = i+1
    MQTT_Topics.append("T" + str(j) + "/onvif-ej/#")
    zones.append("T" + str(j) + '-' + '1')
    zones.append("T" + str(j) + '-' + '2')

db_system.update({'Zones': zones})

vehicles_list = ["Car", "Bike", "Truck"]
zones_list = ["1", "2"]


def mqtt_data_received(msg):
    print(
        "=============================MQTT DATA RECEIVED==============================")
    print("[MQTT TOPIC]: " + msg.topic)
    print("[MQTT MESSAGE]: " + str(msg.payload))
    print('\n')
    parse_mqtt_message(msg.topic, msg.payload)


def input_json_db(json_message):
    json_message_serialized = json.dumps(json_message)
    print("[DATABASE INPUT]: " + str(json_message_serialized))
    db_camera.insert(json.loads(json_message_serialized))
    print(
        "==========================DATA INSERTED IN DATABASE==========================" + "\n\n\n")


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

    if Topic_array[2] == 'RuleEngine':
        if Topic_array[4] == 'Counter':
            rule = msg_deserialized['Source']['Rule']
            rule_split = rule.split()

            if len(rule_split) == 3 and rule_split[1] in vehicles_list and rule_split[2] in zones_list :
                _task = 'Counter'
                _vehicle = rule_split[1]
                _zone = _cam + '-' + rule_split[2]
                _count = msg_deserialized['Data']['Count']

                json_message = create_RuleEngine_message(_cam, _utc_time, _task, _vehicle, _zone, _count)
                input_json_db(json_message)

        '''
        elif Topic_array[4] == 'OccupancyCounter':
            Rule = msg_deserialized['Source']['Rule']
            Rule_split = Rule.split()

            json_message = {
                "Cam": Topic_array[0],
                "UtcTime": msg_deserialized['UtcTime'],
                "Task": "Jam Detection",
                "Zone": Topic_array[0] + '-' + Rule_split[2],
                "Count": msg_deserialized['Data']['Count'],
            }

            input_json_db(json_message)
        '''   
    
    elif Topic_array[2] == 'IVA':
        name = Topic_array[4]
        name_split = name.split()

        if Topic_array[4] == 'Jam 1' or Topic_array[4] == 'Jam 2':

            if len(name_split) == 2:
                _task = 'Jam Detection'
                _zone = _cam + '-' + name_split[1]
                _state = msg_deserialized['Data']['State']

                json_message = create_noVehicle_message(_cam, _utc_time, _task, _zone, _state)
                input_json_db(json_message)
 
        elif Topic_array[3] == 'CrowdDetection':
            
            if Topic_array[4].find('Crowd') != -1 and Topic_array[4].find('Detection') != -1:
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


# Subscribe to all Sensors at Base Topic
def on_connect(client, userdata, flags, rc):
    for i in range(int(n_sensors)):
        client.subscribe(MQTT_Topics[i], 0)


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
client.on_subscribe = on_subscribe
client.username_pw_set(username, password)


