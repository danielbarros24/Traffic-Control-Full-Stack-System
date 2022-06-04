#=======================================================================================================================>
# JSON structure to insert in Database:
# CAM # | onvif-ej | RuleEngine\IVA\VideoSource\Device\Recording |  Task  |  Sub-task  | Rule_name |   Date  |  Data   
#       |          |                                             |        |            |           |         |
# Topic |    \     |                    Topic                    |  Topic |   Topic    |  Message  | Message | Message
#=======================================================================================================================>

from tinydb import TinyDB, Query

db = TinyDB('database/camera_data.json')
query = Query()


#Basic functions

#Inserting
def database_insert(file):
    db.insert(file)

#Getting data
def database_get_all():
    db.all()

def database_iter(db):
    iter(db)

def database_search(query):
    db.search(query)

#Updating
def database_update(fields, query):
    db.update(fields, query)

#Removing
def database_remove(query):
    db.remove(query)

def database_truncate():
    db.truncate()

#Quering
def database_create_query():
    Query()




