# ------------------------------------------
# ---Only to test a simple system-----------
# ------------------------------------------

import paho.mqtt.client as mqtt
from database_manager import database_insert, database_remove, database_create_query, database_get_all, database_iter, database_search, database_truncate, database_update

import json
# from store_data_into_db import sensor_Data_Handler
# from tiny_db_manager import Data_handler

# MQTT Settings
MQTT_Broker = "192.168.1.199"
MQTT_Port = 1883
Keep_Alive_Interval = 40
n_sensors = 1

# Server Credentials
username = "daniel"
password = "password"

MQTT_Topics = []
for i in range(n_sensors):
    j = i+1
    MQTT_Topics.append("T" + str(j) + "/onvif-ej/#")

print(MQTT_Topics)
# TOPICS

def mqtt_data_received (msg):
    print(
        "=============================MQTT DATA RECEIVED==============================")
    print("[MQTT TOPIC]: " + msg.topic)
    print("[MQTT MESSAGE]: " + str(msg.payload))
    print('\n\n')
    parse_mqtt_message(msg.topic, msg.payload)


def input_json_db(json_message):
    json_message_serialized = json.dumps(json_message)
    print("[DATABASE INPUT]: " + str(json_message_serialized))
    database_insert(json.loads(json_message_serialized))
    print(
        "==========================DATA INSERTED IN DATABASE==========================" + "\n\n")

# Parses the Mqtt Topic


def parse_mqtt_message(topic, message):

    Topic_array = []
    Topic_array = topic.split("/")
    msg_deserialized = json.loads(message)

    if Topic_array[2] == 'RuleEngine':
        if Topic_array[4] == 'Counter':
            Rule = msg_deserialized['Source']['Rule']
            Rule_split = Rule.split()

            json_message = {
                "Cam": Topic_array[0],
                "UtcTime": msg_deserialized['UtcTime'],
                "Task": Topic_array[4],
                "Vehicle": Rule_split[0],
                "Zone": Topic_array[0] + '-' + Rule_split[2],
                "Count": msg_deserialized['Data']['Count'],
            }

            input_json_db(json_message)

        elif Topic_array[4] == 'Occupancy Counter':
            Rule = msg_deserialized['Source']['Rule']
            Rule_split = Rule.split()

            json_message = {
                "Cam": Topic_array[0],
                "UtcTime": msg_deserialized['UtcTime'],
                "Task": Topic_array[4],
                "Vehicle": Rule_split[0],
                "Zone": Topic_array[0] + '-' + Rule_split[2],
                "Count": msg_deserialized['Data']['Count'],
            }

            input_json_db(json_message)

    elif Topic_array[2] == 'IVA':
        if msg_deserialized['Data']['State'] == 'true':
            if Topic_array[2] == 'CrowdDetection':
                json_message = {
                    "Cam": Topic_array[0],
                    "UtcTime": msg_deserialized['UtcTime'],
                    "Task": 'Crowd Detection',
                    "State": msg_deserialized['Data']['State'],
                }
                input_json_db(json_message)

            if Topic_array[4] == 'Idle_Truck':
                json_message = {
                    "Cam": Topic_array[0],
                    "UtcTime": msg_deserialized['UtcTime'],
                    "Task": Topic_array[4],
                    "Vehicle": 'Truck',
                    "State": msg_deserialized['Data']['State'],
                }
                input_json_db(json_message)

            if Topic_array[4] == 'Idle_Car':
                json_message = {
                    "Cam": Topic_array[0],
                    "UtcTime": msg_deserialized['UtcTime'],
                    "Task": Topic_array[4],
                    "Vehicle": 'Car',
                    "State": msg_deserialized['Data']['State'],
                }
                input_json_db(json_message)



# Subscribe to all Sensors at Base Topic
def on_connect(client, userdata, flags, rc):
    for i in range(n_sensors):
        client.subscribe(MQTT_Topics[i], 0)

# Save Data into DB Table


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


# Connect
client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))


# Continue the network loop
client.loop_forever()
