#------------------------------------------
#---Only to test a simple system-----------
#------------------------------------------

import paho.mqtt.client as mqtt
from database_manager import database_insert, database_remove, database_create_query, database_get_all, database_iter, database_search, database_truncate, database_update
import json
#from store_data_into_db import sensor_Data_Handler
#from tiny_db_manager import Data_handler

# MQTT Settings 
MQTT_Broker = "192.168.1.199"
MQTT_Port = 1883
Keep_Alive_Interval = 40
MQTT_Topic = "BoschCam1/#"

#Server Credentials
username = "daniel"
password = "password"


#Parses the Mqtt Topic
def parse_mqtt_message(topic, message):

	Topic_array = []
	Topic_array = topic.split("/")

	msg_deserialized = json.loads(message)

	Source = msg_deserialized['Source']['VideoSource']

	DB_row = {
		"Cam": Topic_array[0],
		"UtcTime": msg_deserialized['UtcTime'],
		"Topic":Topic_array[2],
		"Task":Topic_array[3],
		"Subtask":Topic_array[4],
		"Data": msg_deserialized['Data']
	}

	DB_row_json = json.dumps(DB_row)
	print("[DATABASE INPUT]: " + str(DB_row_json))

	database_insert(json.loads(DB_row_json))
	print("==========================DATA INSERTED IN DATABASE==========================" + "\n\n")
	

#Subscribe to all Sensors at Base Topic
def on_connect(client, userdata, flags, rc):
	client.subscribe(MQTT_Topic, 0)


#Save Data into DB Table
def on_message(client, userdata, msg):

	print("=============================MQTT DATA RECEIVED==============================")
	print("[MQTT TOPIC]: " + msg.topic)
	print("[MQTT MESSAGE]: " + str(msg.payload))
	parse_mqtt_message(msg.topic, msg.payload)
	


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

