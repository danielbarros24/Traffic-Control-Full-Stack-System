#------------------------------------------
#---Only to test a simple system-----------
#------------------------------------------


import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

#====================================================
# MQTT Settings 
MQTT_Broker = "192.168.1.199"
MQTT_Port = 1883
Keep_Alive_Interval = 45

MQTT_Topic_RuleEngine = "BoschCam1/onvif-ej/RuleEngine/CountAgregation/Counter/&1"
MQTT_Topic_IVA = "BoschCam1/onvif-ej/IVA/"
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
	threading.Timer(1.0, publish_Cam_Events_to_MQTT).start()
	UtcTime = datetime.now()
	Count = random.randint(0,500)


	Cam_Data = {
		"UtcTime": UtcTime.isoformat(),
		"Source":
			{"VideoSource":1,"Rule":"counter 4"},
		"Data":
			{"Count":Count}
	}

	Cam_Data_json = json.dumps(Cam_Data)
	publish_To_Topic (MQTT_Topic_RuleEngine, Cam_Data_json)


publish_Cam_Events_to_MQTT()

#====================================================
