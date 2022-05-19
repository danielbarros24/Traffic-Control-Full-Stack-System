from tinydb import TinyDB, Query

# DATABASE
db_camera = TinyDB('../database/camera_data.json')
db_auth = TinyDB('../database/auth.json')
db_auto = TinyDB('../database/automations.json')
db_general = TinyDB('../database/general_info.json')

query = Query()

