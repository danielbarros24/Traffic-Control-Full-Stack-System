#------------------------------------------
#---Only to test a simple system-----------
#------------------------------------------


import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime
import time
#====================================================
# MQTT Settings 
MQTT_Broker = "192.168.1.199"
MQTT_Port = 1883
Keep_Alive_Interval = 45

MQTT_Topic_RuleEngine = "T1/onvif-ej/RuleEngine/CountAgregation/Counter/&1/Truck Counter 1"
MQTT_Topic_IVA = "T1/onvif-ej/IVA/IdleObject/Idle_Truck/&1"
MQTT_Topic_JamDetection = "T1/onvif-ej/RuleEngine/CountAgregation/OccupancyCounter/&1/Jam Detection 1"
MQTT_Topic_IVA_Crowd_Detection = "T1/onvif-ej/IVA/CrowdDetection/Crowd Detection/&1"

MQTT_Topic_VideoSource = "BoschCam1/onvif-ej/VideoSource/"
MQTT_Topic_Device = "BoschCam1/onvif-ej/Device/"
MQTT_Topic_Recording = "BoschCam1/onvif-ej/Recording/"


#Server Credentials
username = "daniel"
password = "password"

#====================================================

def on_connect(client, userdata, flags, rc):
	if rc != 0:
		pass
		print("Unable to connect to MQTT Broker...")
	else:
		print("Connected with MQTT Broker: " + str(MQTT_Broker))


def on_publish(client, userdata, mid):
	pass
		
def on_disconnect(client, userdata, rc):
	if rc !=0:
		pass
		

client = mqtt.Client("mqtt-data-publisher")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.username_pw_set(username, password)
client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))		

		
def publish_To_Topic(topic, message):
	client.publish(topic,message)
	print("Published!")
	print("[MQTT TOPIC]: " + str(topic))
	print("[MESSAGE]: " + str(message) + "\n")



#====================================================
#Generate fake event values


def publish_Cam_Events_to_MQTT():
	
	UtcTime = datetime.now()
	Count = random.randint(0,500)

	UtcTime = UtcTime.isoformat() + 'Z'
	Cam_Data_IVA_Crowd_True = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"true"}
	}
	Cam_Data_json_1 = json.dumps(Cam_Data_IVA_Crowd_True)
	publish_To_Topic (MQTT_Topic_IVA_Crowd_Detection, Cam_Data_json_1)

	time.sleep(4)

	UtcTime = datetime.now()
	UtcTime = UtcTime.isoformat() + 'Z'
	Cam_Data_IVA_Crowd_True = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"false"}
	}
	Cam_Data_json_2 = json.dumps(Cam_Data_IVA_Crowd_True)
	publish_To_Topic (MQTT_Topic_IVA_Crowd_Detection, Cam_Data_json_2)

	time.sleep(4)
	
	'''
	UtcTime = UtcTime.isoformat() + 'Z'
	Cam_Data_IVA_true = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"true"}
	}
	Cam_Data_json_2 = json.dumps(Cam_Data_IVA_true)
	publish_To_Topic (MQTT_Topic_IVA, Cam_Data_json_2)

	time.sleep(4)

	UtcTime = datetime.now()
	UtcTime = UtcTime.isoformat() + 'Z'
	Cam_Data_IVA_false = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"false"}
	}
	Cam_Data_json_1 = json.dumps(Cam_Data_IVA_false)
	publish_To_Topic (MQTT_Topic_IVA, Cam_Data_json_1)

	time.sleep(4)
	
	Cam_Data_Rule = {
		"UtcTime": UtcTime,
		"Source":
			{"VideoSource":"1","Rule":"Truck Counter 1"},
		"Data":
			{"Count":Count}
	}
	Cam_Data_json = json.dumps(Cam_Data_Rule)
	publish_To_Topic (MQTT_Topic_RuleEngine, Cam_Data_json)

	Cam_Data_Jam = {
		"UtcTime": UtcTime,
		"Source":
			{"VideoSource":"1","Rule":"Jam Detection 1"},
		"Data":
			{"Count":"0"}
	}
	Cam_Data_json = json.dumps(Cam_Data_Jam)
	publish_To_Topic (MQTT_Topic_JamDetection, Cam_Data_json)

'''
while True:
	publish_Cam_Events_to_MQTT()

#====================================================
