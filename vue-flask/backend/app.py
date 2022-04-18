from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
Cors = CORS(app)

CORS(app, resources={r'/*': {'origins':
 '*'}}, CORS_SUPPORTS_CREDENTIALS=True)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.post("/dataentry")
def submitData():  
    response_object = {'status': 'success'} 
    
    post_data = request.get_json()     
    username = post_data.get('username'),     
    password = post_data.get('password') 

    print(username) 
    print(password)     

    response_object['message'] = 'Data added!'

    return response_object

