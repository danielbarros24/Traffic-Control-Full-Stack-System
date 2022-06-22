import time
from mqtt.mqtt import client, set_flag
from process_trigger.process_trigger import test_automations

from tinydb import TinyDB, Query, where 

db_system = TinyDB('database/system.json')

ip = [query.get('Broker_IP') for query in db_system.all()]

# MQTT Settings
MQTT_Broker = ip[0]
MQTT_Port = 1883
Keep_Alive_Interval = 30


# Connect
connected = False
try:
    client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
    print("MQTT BROKER CONNECTION ESTABLISHED!")
    db_system.update({'mqtt_connection': "ok"})
    connected = True
    client.loop_start()
    
except: 
    print("MQTT BROKER CONNECTION FAILED!")
    db_system.update({'mqtt_connection': "failed"})
    connected = False
    

while True:

    if connected:
        if set_flag() == 1:
            db_system.update({'mqtt_connection': "ok"})
            test_automations()
            time.sleep(1)
        else:
            print("CONNECTION FAILED")
            db_system.update({'mqtt_connection': "failed"})
            #test_automations()
            time.sleep(1)
    else: 
        print("CONNECTION FAILED")
        db_system.update({'mqtt_connection': "failed"})
        print("Trying to reconnect in 5 seconds...")
        time.sleep(5)
        try:
            client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
            print("MQTT BROKER CONNECTION ESTABLISHED!")
            db_system.update({'mqtt_connection': "ok"})
            connected = True
            client.loop_start()
            
        except: 
            print("MQTT BROKER CONNECTION FAILED!")
            db_system.update({'mqtt_connection': "failed"})
            connected = False
        

        


