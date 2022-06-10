#### Iterar por cada automação e verificar se enable e a data estão ON. Se sim -> verificar as variáveis. Se não -> avança
#### Buscar na DB da camara os dados e ver a condiçao presente na DB de automações.
#### Construir JSON dos dados: {"data": { "fluxo1" : 100, "fluxo2" : 60}}
#### Executa jsonLogic.apply(rules, data);
#### Retorna true ou false -> se true coloca pino x a 1

import json
from datetime import datetime
from ssl import VerifyFlags
import pytz
from dateutil import parser
from tinydb import Query, TinyDB, where

from .json_logic import jsonLogic


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

    utc=pytz.UTC

    #docs = db_auto.search(where('enable') == True)
    docs = db_processes.all()
    current_date = datetime.now()
    current_date = current_date.replace(tzinfo=utc)
    
    
    if not docs:
        print("No processes configured")

    for doc in docs:
        raw_start_time = doc.get('startTime')

        startTime = parser.parse(raw_start_time)
        endTime = parser.parse(doc.get('endTime'))
        enable = doc.get('enable')

        pins_info = doc.get('gpios')
        pins = []

        for item in pins_info:
            pin = item.get('gpio')
            pins.append(pin)

        

        if(compare_datetime(current_date, startTime, endTime) and enable == True):

            

            triggering = doc.get('triggering')


            db_general.update({"start_time": "{}".format(raw_start_time)})
            rules = doc.get('rules') 

            print("Verifying " + str(doc.get('name') + " process..."))

            if jsonLogic(rules):
                print("Process Triggered: " + str(doc.get('name')) + " | " "Activated pins: " + str(pins) + "\n")

                if(triggering == True):             #PROCESS IS STILL TRUE
                    print("PROCESS IS STILL TRUE")

                else:                               #RISING EDGE - PROCESS WAS FALSE AND NOW IS TRUE
                    doc.update({"triggering": True})
                    doc.update({"notification": True})
                    doc.update({"lastTimeTriggerStart": "{}".format(current_date)})
                    
                    print("RISING EDGE")
            else:
                if(triggering == True):             #FALLING EDGE - PROCESS NOT TRUE ANYMORE
                    doc.update({"triggering": False}) 
                    doc.update({"lastTimeTriggerStop": "{}".format(current_date)})
                    print("FALLING EDGE")
                    #TURN OFF PROCESS PINS
                else:                               #PROCESS IS STILL FALSE
                    print("PROCESS IS STILL FALSE\n")

        #elif(compare_datetime(current_date, startTime, endTime) == False or enable == False):
            #TURN OFF pins[]


