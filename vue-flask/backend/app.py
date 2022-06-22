import time
from mqtt.mqtt import client, flag_connected
from process_trigger.process_trigger import test_automations

from tinydb import TinyDB, Query, where 

db_system = TinyDB('database/system.json')

ip = [query.get('Broker_IP') for query in db_system.all()]

# MQTT Settings
MQTT_Broker = ip[0]
MQTT_Port = 1883
Keep_Alive_Interval = 40


# Connect
connected = False
try:
    rc = client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
    print("MQTT BROKER CONNECTION ESTABLISHED!")
    db_system.update({'mqtt_connection': "ok"})
    connected = True
except: 
    print("MQTT BROKER CONNECTION FAILED!")
    db_system.update({'mqtt_connection': "failed"})
    connected = False

while True:

    if connected:
        client.loop_start()
        if flag_connected == 0: 
            print("CONNECTION OK")

            db_system.update({'mqtt_connection': "ok"})

            test_automations()

            time.sleep(1)
        else:
            print("ERROS")
    else: 
        test_automations()

        print("CONNECTION FAILED")

        db_system.update({'mqtt_connection': "failed"})

        time.sleep(1)
        


