from tinydb import TinyDB, Query
import json

db = TinyDB('db.json')

Cam = Query()

#=============================>
# JSON structure to insert in Database:
# CAM # | onvif-ej | RuleEngine\IVA\VideoSource\Device\Recording |  Task  |  Sub-task  | Rule_name |   Date  | Data   
#       |          |                                             |        |            |           |         |
# Topic |    \     |                    Topic                    |  Topic |   Topic    |  Message  | Message | Message