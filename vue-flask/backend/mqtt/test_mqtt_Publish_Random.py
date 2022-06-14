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

######################################  MQTT TOPICS ################################################

MQTT_Topic_truck_counter_1 = "T1/onvif-ej/RuleEngine/CountAgregation/Counter/&1/Counter Truck 1"
MQTT_Topic_truck_counter_2 = "T1/onvif-ej/RuleEngine/CountAgregation/Counter/&1/Counter Truck 1"

MQTT_Topic_car_counter_1 = "T1/onvif-ej/RuleEngine/CountAgregation/Counter/&1/Counter Car 1"
MQTT_Topic_car_counter_2 = "T1/onvif-ej/RuleEngine/CountAgregation/Counter/&1/Counter Car 2"

MQTT_Topic_bike_counter_1 = "T1/onvif-ej/RuleEngine/CountAgregation/Counter/&1/Counter Bike 1"
MQTT_Topic_bike_counter_2 = "T1/onvif-ej/RuleEngine/CountAgregation/Counter/&1/Counter Bike 2"


MQTT_Topic_IVA_double_park_car_1 = "T2/onvif-ej/IVA/IdleObject/&1/DoublePark Car 1"
MQTT_Topic_IVA_double_park_car_2 = "T2/onvif-ej/IVA/IdleObject/&1/DoublePark Car 2"

MQTT_Topic_IVA_double_park_truck_1 = "T2/onvif-ej/IVA/IdleObject/&1/DoublePark Truck 1"
MQTT_Topic_IVA_double_park_truck_2 = "T2/onvif-ej/IVA/IdleObject/&1/DoublePark Truck 2"

MQTT_Topic_IVA_double_park_bike_1 = "T2/onvif-ej/IVA/IdleObject/&1/DoublePark Bike 1"
MQTT_Topic_IVA_double_park_bike_2 = "T2/onvif-ej/IVA/IdleObject/&1/DoublePark Bike 2"


MQTT_Topic_IVA_idle_car_1 = "T2/onvif-ej/IVA/IdleObject/&1/Idle Car 1"
MQTT_Topic_IVA_idle_car_2 = "T2/onvif-ej/IVA/IdleObject/&1/Idle Car 2"

MQTT_Topic_IVA_idle_truck_1 = "T2/onvif-ej/IVA/IdleObject/&1/Idle Truck 1"
MQTT_Topic_IVA_idle_truck_2 = "T2/onvif-ej/IVA/IdleObject/&1/Idle Truck 2"

MQTT_Topic_IVA_idle_bike_1 = "T2/onvif-ej/IVA/IdleObject/&1/Idle Bike 1"
MQTT_Topic_IVA_idle_bike_2 = "T1/onvif-ej/IVA/IdleObject/&1/Idle Bike 2"


MQTT_Topic_IVA_jam_1 = "T2/onvif-ej/IVA/ObjectInField/&1/Jam 1"
MQTT_Topic_IVA_jam_2 = "T1/onvif-ej/IVA/ObjectInField/&1/Jam 2"


MQTT_Topic_IVA_Crowd_Detection = "T1/onvif-ej/IVA/CrowdDetection/&1/Crowd Detection"

##################################################################################################


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

	
	Cam_Data_IVA_idle_car= {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"true"}
	}
	Cam_Data_json = json.dumps(Cam_Data_IVA_idle_car)
	publish_To_Topic (MQTT_Topic_IVA_idle_car_1, Cam_Data_json)

	time.sleep(1)
	Cam_Data_IVA_idle_car = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"false"}
	}
	Cam_Data_json = json.dumps(Cam_Data_IVA_idle_car)
	publish_To_Topic (MQTT_Topic_IVA_idle_car_1, Cam_Data_json)

	time.sleep(1)

	Cam_Data_IVA_idle_truck = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"false"}
	}
	Cam_Data_json = json.dumps(Cam_Data_IVA_idle_truck)
	publish_To_Topic (MQTT_Topic_IVA_idle_truck_2, Cam_Data_json)

	time.sleep(1)

	Cam_Data_IVA_idle_truck = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"true"}
	}
	Cam_Data_json = json.dumps(Cam_Data_IVA_idle_truck)
	publish_To_Topic (MQTT_Topic_IVA_idle_car_2, Cam_Data_json)

	time.sleep(1)

	Cam_Data_IVA_double_park= {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"true"}
	}
	Cam_Data_json = json.dumps(Cam_Data_IVA_double_park)
	publish_To_Topic (MQTT_Topic_IVA_double_park_bike_1, Cam_Data_json)

	time.sleep(1)
	Cam_Data_IVA_double_park = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"true"}
	}
	Cam_Data_json = json.dumps(Cam_Data_IVA_double_park)
	publish_To_Topic (MQTT_Topic_IVA_double_park_bike_2, Cam_Data_json)

	time.sleep(1)

	Cam_Data_IVA_Crowd_True = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"true"}
	}
	Cam_Data_json_1 = json.dumps(Cam_Data_IVA_Crowd_True)
	publish_To_Topic (MQTT_Topic_IVA_Crowd_Detection, Cam_Data_json_1)

	time.sleep(1)

	UtcTime = datetime.now()
	UtcTime = UtcTime.isoformat() + 'Z'

	time.sleep(1)

	Cam_Data_Rule = {
		"UtcTime": UtcTime,
		"Source":
			{"VideoSource":"1","Rule":"Counter Truck 1"},
		"Data":
			{"Count":Count}
	}
	Cam_Data_json = json.dumps(Cam_Data_Rule)
	publish_To_Topic (MQTT_Topic_truck_counter_1, Cam_Data_json)
	time.sleep(1)

	Cam_Data_Rule = {
		"UtcTime": UtcTime,
		"Source":
			{"VideoSource":"1","Rule":"Counter Car 1"},
		"Data":
			{"Count":Count}
	}
	Cam_Data_json = json.dumps(Cam_Data_Rule)
	publish_To_Topic (MQTT_Topic_car_counter_1, Cam_Data_json)
	time.sleep(1)

	Cam_Data_Rule = {
		"UtcTime": UtcTime,
		"Source":
			{"VideoSource":"1","Rule":"Counter Bike 2"},
		"Data":
			{"Count":Count}
	}
	Cam_Data_json = json.dumps(Cam_Data_Rule)
	publish_To_Topic (MQTT_Topic_bike_counter_2, Cam_Data_json)
	time.sleep(1)

	Cam_Data_Jam = {
			"UtcTime": UtcTime,
			"Source":
				{"Source":"1"},
			"Data":
				{"State":"true"}
		}
	Cam_Data_json = json.dumps(Cam_Data_Jam)
	publish_To_Topic (MQTT_Topic_IVA_jam_1, Cam_Data_json)

	time.sleep(1)

	Cam_Data_Jam = {
		"UtcTime": UtcTime,
		"Source":
			{"Source":"1"},
		"Data":
			{"State":"false"}
	}
	Cam_Data_json = json.dumps(Cam_Data_Jam)
	publish_To_Topic (MQTT_Topic_IVA_jam_2, Cam_Data_json)
	time.sleep(1)

	'''
################### DOUBLE PARK #################################
	Cam_Data_IVA_double_park= {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"true"}
	}
	Cam_Data_json = json.dumps(Cam_Data_IVA_double_park)
	publish_To_Topic (MQTT_Topic_IVA_double_park_bike_1, Cam_Data_json)

	time.sleep(1)
	Cam_Data_IVA_double_park = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"true"}
	}
	Cam_Data_json = json.dumps(Cam_Data_IVA_double_park)
	publish_To_Topic (MQTT_Topic_IVA_double_park_bike_2, Cam_Data_json)

	time.sleep(1)

#####################################################################

################### CROWD DETECTION #################################

	Cam_Data_IVA_Crowd_True = {
		"UtcTime": UtcTime,
		"Source":
			{"Source": "1"},
		"Data":
			{"State":"true"}
	}
	Cam_Data_json_1 = json.dumps(Cam_Data_IVA_Crowd_True)
	publish_To_Topic (MQTT_Topic_IVA_Crowd_Detection, Cam_Data_json_1)

	time.sleep(1)

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

	time.sleep(1)
	
#####################################################################

#####################################################################
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

########################## Counters #############################
	Cam_Data_Rule = {
		"UtcTime": UtcTime,
		"Source":
			{"VideoSource":"1","Rule":"Counter Truck 1"},
		"Data":
			{"Count":Count}
	}
	Cam_Data_json = json.dumps(Cam_Data_Rule)
	publish_To_Topic (MQTT_Topic_truck_counter_1, Cam_Data_json)
	time.sleep(1)

	Cam_Data_Rule = {
		"UtcTime": UtcTime,
		"Source":
			{"VideoSource":"1","Rule":"Counter Car 1"},
		"Data":
			{"Count":Count}
	}
	Cam_Data_json = json.dumps(Cam_Data_Rule)
	publish_To_Topic (MQTT_Topic_car_counter_1, Cam_Data_json)
	time.sleep(1)

	Cam_Data_Rule = {
		"UtcTime": UtcTime,
		"Source":
			{"VideoSource":"1","Rule":"Counter bike 2"},
		"Data":
			{"Count":Count}
	}
	Cam_Data_json = json.dumps(Cam_Data_Rule)
	publish_To_Topic (MQTT_Topic_bike_counter_2, Cam_Data_json)
	time.sleep(1)


########################## Jam #############################
	Cam_Data_Jam = {
			"UtcTime": UtcTime,
			"Source":
				{"Source":"1"},
			"Data":
				{"State":"true"}
		}
		Cam_Data_json = json.dumps(Cam_Data_Jam)
		publish_To_Topic (MQTT_Topic_IVA_jam_1, Cam_Data_json)

		time.sleep(1)

		Cam_Data_Jam = {
			"UtcTime": UtcTime,
			"Source":
				{"Source":"1"},
			"Data":
				{"State":"false"}
		}
		Cam_Data_json = json.dumps(Cam_Data_Jam)
		publish_To_Topic (MQTT_Topic_IVA_jam_2, Cam_Data_json)
		time.sleep(1)
'''

while True:

	publish_Cam_Events_to_MQTT()

#====================================================
