#------------------------------------------
#---Only to test a simple system-----------
#------------------------------------------

import paho.mqtt.client as mqtt
import json
#from store_data_into_db import sensor_Data_Handler
#from tiny_db_manager import Data_handler

# MQTT Settings 
MQTT_Broker = "192.168.1.199"
MQTT_Port = 1883
Keep_Alive_Interval = 40
MQTT_Topic = "Cam1/#"

#Server Credentials
username = "daniel"
password = "password"


#Parses the Mqtt Topic
def parse_mqtt_message(topic, message):

	Topic_array = []
	Topic_array = topic.split("/")
	print("[Deserialized Topic]:" + str(Topic_array))

	msg_deserialized = json.loads(message)

	Source = msg_deserialized['Source']['VideoSource']

	DB_row = {
		"Cam": Topic_array[0],
		"UtcTime": msg_deserialized['UtcTime'],
		"Topic":Topic_array[2],
		"Task":Topic_array[3],
		"Sub-task":Topic_array[4],
		"Data": msg_deserialized['Data']
	}

	print("Source: " + str(Source))	
	DB_row_json = json.dumps(DB_row)
	print("[INPUT DB]: " + str(DB_row_json))

#Subscribe to all Sensors at Base Topic
def on_connect(client, userdata, flags, rc):
	client.subscribe(MQTT_Topic, 0)


#Save Data into DB Table
def on_message(client, userdata, msg):

	print("MQTT Data Received!")
	print("[MQTT TOPIC]: " + msg.topic)
	parse_mqtt_message(msg.topic, msg.payload)
	print("[MQTT MESSAGE]: " + str(msg.payload) + "\n")


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

