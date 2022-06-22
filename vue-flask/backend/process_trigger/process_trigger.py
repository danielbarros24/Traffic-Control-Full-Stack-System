#### Iterar por cada automação e verificar se enable e a data estão ON. Se sim -> verificar as variáveis. Se não -> avança
#### Buscar na DB da camara os dados e ver a condiçao presente na DB de automações.
#### Construir JSON dos dados: {"data": { "fluxo1" : 100, "fluxo2" : 60}}
#### Executa jsonLogic.apply(rules, data);
#### Retorna true ou false -> se true coloca pino x a 1

import json
from datetime import datetime, timezone
from ssl import VerifyFlags
import pytz
from dateutil import parser
from tinydb import Query, TinyDB, where

from .json_logic import jsonLogic

########## GPIO SETUP ############
#import RPi.GPIO as GPIO 

#GPIO.setmode(GPIO.BCM)

#gpio_list = [4 ,5 ,6 ,7 ,8 ,9 ,10 ,11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

#for p in gpio_list:
#    GPIO.setup(p, GPIO.OUT)


#===============================================================================================================
# DATABASE
db_camera = TinyDB('database/camera.json')
db_auth = TinyDB('database/auth.json')
db_processes = TinyDB('database/processes.json')
db_general = TinyDB('database/system.json')

query = Query()

startTime = ""

def compare_datetime(current_date, start_time, end_time):
    if current_date > start_time and current_date < end_time:
        return True
    else:
        return False


def test_automations():

    #utc=pytz.UTC

    docs = db_processes.all()
    current_date = datetime.now(timezone.utc)

    if not docs:
        print("No processes configured")

    for doc in docs:
        raw_start_time = doc.get('startTime')

        startTime = parser.parse(raw_start_time)
        endTime = parser.parse(doc.get('endTime'))
        enable = doc.get('enable')

        pins_info = doc.get('gpios')
        all_pins = []
        normal_pins = []
        inverted_pins = []

        for item in pins_info:
            pin = item.get('gpio')
            all_pins.append(pin)
            if item.get('inverted') == False:
                normal_pins.append(pin)
            else:
                inverted_pins.append(pin)
        

        if(compare_datetime(current_date, startTime, endTime) and enable == True):

            triggering = doc.get('triggering')

            db_general.update({"start_time": "{}".format(raw_start_time)})

            rules = doc.get('rules') 

            print("Verifying " + str(doc.get('name') + " process..."))

            if jsonLogic(rules):

                if(triggering == True):             #PROCESS IS STILL TRUE
                    print("PROCESS " + str(doc.get('name')) + " IS STILL TRUE" + '\n')

                else:                               #RISING EDGE - PROCESS WAS FALSE AND NOW IS TRUE
                    doc.update({"triggering": True})
                    doc.update({"notification": True})
                    doc.update({"lastTimeTrigger": "{}".format(current_date)})
                    
                    db_processes.update(doc, doc_ids=[int(doc.doc_id)])

                    print("RISING EDGE")
                    print("PROCESS START TRIGGERING: " + str(doc.get('name')))
                    print("TURN ON NOT INVERTED PINS " + str(normal_pins))
                    print("TURN OFF INVERTED PINS " + str(inverted_pins) + '\n')

                    #for g1 in normal_pins:
                    #   GPIO.output(g1, 1)

                    #for g1_n in inverted_pins:
                    #   GPIO.output(g1_n, 0)

            else:
                if(triggering == True):             #FALLING EDGE - PROCESS NOT TRUE ANYMORE
                    doc.update({"triggering": False})
                    db_processes.update(doc, doc_ids=[int(doc.doc_id)])

                    print("FALLING EDGE")
                    print("PROCESS STOP TRIGGERING: " + str(doc.get('name')))
                    print("TURN OFF NOT INVERTED PINS " + str(normal_pins))
                    print("TURN ON INVERTED PINS " + str(inverted_pins) + '\n')

                    #for g2 in normal_pins:
                    #   GPIO.output(g2, 0)

                    #for g2_n in inverted_pins:
                    #   GPIO.output(g2_n, 1)

                else:                               #PROCESS IS STILL FALSE
                    print("PROCESS " + str(doc.get('name')) + " IS STILL FALSE" + '\n')

        elif(compare_datetime(current_date, startTime, endTime) == False or enable == False):
            print("PROCESS " + str(doc.get('name') + " is OFF"))
            print("TURN OFF " + str(doc.get('name')) + " PINS: " + str(all_pins) + '\n')
            
            #for g3 in all_pins:
            #   GPIO.output(g3, 0)

    #UPDATE VEHICLE DETECTION VALUES
    doc_system = db_general.all()[0]
    last_car_count = doc_system.get('jsonLogicCarCount')
    last_truck_count = doc_system.get('jsonLogicTruckCount')
    last_bike_count = doc_system.get('jsonLogicBikeCount')
    
    db_general.update({'lastCarCount': last_car_count})
    db_general.update({'lastTruckCount': last_truck_count})
    db_general.update({'lastBikeCount': last_bike_count})