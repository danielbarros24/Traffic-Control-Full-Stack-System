import time
from mqtt.mqtt import client
from process_trigger.process_trigger import test_automations

from tinydb import TinyDB, Query, where 

db_system = TinyDB('database/system.json')

ip = [query.get('Broker_IP') for query in db_system.all()]

# MQTT Settings
MQTT_Broker = ip[0]
MQTT_Port = 1883
Keep_Alive_Interval = 40

# Connect
client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

while True:
    
    # Continue the network loop
    client.loop_start()
    test_automations()
    time.sleep(1)


