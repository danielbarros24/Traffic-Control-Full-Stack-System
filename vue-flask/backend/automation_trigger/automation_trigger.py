#### Iterar por cada automação e verificar se enable e a data estão ON. Se sim -> verificar as variáveis. Se não -> avança
#### Buscar na DB da camara os dados e ver a condiçao presente na DB de automações.
#### Construir JSON dos dados: {"data": { "fluxo1" : 100, "fluxo2" : 60}}
#### Executa jsonLogic.apply(rules, data);
#### Retorna true ou false -> se true coloca pino x a 1


import json
from datetime import datetime
import pytz
from dateutil import parser
from tinydb import Query, TinyDB, where

from json_logic import jsonLogic


# DATABASE
db_camera = TinyDB('../database/camera_data.json')
db_auth = TinyDB('../database/auth.json')
db_auto = TinyDB('../database/automations.json')
db_general = TinyDB('../database/general_info.json')

query = Query()

startTime = ""

def compare_datetime(current_date, start_time, end_time):
    if current_date > start_time and current_date < end_time:
        return True
    else:
        return False

def test_automations():

    utc=pytz.UTC

    docs = db_auto.search(where('enable') == True)

    current_date = datetime.now()
    current_date = current_date.replace(tzinfo=utc)

    for doc in docs:
        raw_start_time = doc.get('startTime')

        startTime = parser.parse(raw_start_time)
        endTime = parser.parse(doc.get('endTime'))

        if(compare_datetime(current_date, startTime, endTime)):

            db_general.update({"start_time": "{}".format(raw_start_time)})
            rules = doc.get('rules') 

            if jsonLogic(rules):
                print("Process Triggered: " + str(doc.get('name')) + " | " "Activated pins: " + str(doc.get('gpios')))

#while True:
    
test_automations()

    #Awaits until new data is received
