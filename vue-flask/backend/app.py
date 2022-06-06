import time
from mqtt.mqtt import client
from process_trigger.process_trigger import test_automations

# MQTT Settings
MQTT_Broker = "192.168.1.199"
MQTT_Port = 1883
Keep_Alive_Interval = 40

# Connect
client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# Continue the network loop
client.loop_start()

while True:
    test_automations()
    time.sleep(1)


