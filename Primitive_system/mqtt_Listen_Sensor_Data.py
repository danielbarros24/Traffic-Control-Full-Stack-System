#------------------------------------------
#---Only to test a simple system-----------
#------------------------------------------

import paho.mqtt.client as mqtt
from store_data_into_db import sensor_Data_Handler

# MQTT Settings 
MQTT_Broker = "192.168.1.199"
MQTT_Port = 1883
Keep_Alive_Interval = 40
MQTT_Topic = "Home/BedRoom/#"

#Server Credentials
username = "daniel"
password = "password"


#Subscribe to all Sensors at Base Topic
def on_connect(client, userdata, flags, rc):
	client.subscribe(MQTT_Topic, 0)

#Save Data into DB Table
def on_message(client, userdata, msg):
	# This is the Master Call for saving MQTT Data into DB
	# For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
	print("MQTT Data Received...")
	print("MQTT Topic: " + msg.topic)
	print("Data: " + str(msg.payload))
	sensor_Data_Handler(msg.topic, msg.payload)

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
