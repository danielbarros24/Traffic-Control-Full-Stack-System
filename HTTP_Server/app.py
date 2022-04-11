from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

i = 0

@app.route("/")
def hello_world():
    global i
    i=i+1
    return {
        "idade": i,
        "nome": "João"
    }