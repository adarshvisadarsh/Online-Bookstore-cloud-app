from flask import Flask, render_template, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
from datetime import datetime
import re
import os
import json

aws_instance_ip = "18.213.176.85"
app = Flask(__name__)
cors = CORS(app)
client = MongoClient("mongodb://dbuser:dbpwd@" + aws_instance_ip + "/books_db")
db = client.books_db
collection = db["books"]


@app.route('/catalogue-service', methods=['POST', 'GET'])
def catalogue_service():
    #  create a catalogue json file if not present
    # else append
    path = os.getcwd()
    req_body = request.json
    data = req_body["data"]
    with open('data.json', 'a') as f:
        json.dump(data, f)
    return "written success"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
