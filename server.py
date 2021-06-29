from flask import Flask, render_template, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
from datetime import datetime
import requests
import re
import os
import json

base_url = 'http://127.0.0.1'
app = Flask(__name__)
cors = CORS(app)
client = MongoClient("mongodb+srv://admin:U9gyl4m0gWCzPeEO@cluster0.36gi7.mongodb.net/book_db?retryWrites=true&w=majority")
db = client['book_db']
collection = db["books"]

def update_search_log(searchstring):
    # cerate a text file and write the keyoword with timestamp
    search_time = datetime.now().time()
    data_string = str(searchstring) + " : " + str(search_time)
    counter = 0
    data_lines = []
    try:
        with open('search_log.txt') as log_file:
            data_lines = log_file.readlines()

        print(data_lines)
    except FileNotFoundError:
        print("File Not found")

    for line in data_lines:
        if searchstring in line:
            counter += 1

    counter += 1
    data_string = data_string + str(" Total count: " + str(counter) + ".\n")
    data_lines.append(data_string)
    with open('search_log.txt', 'w') as log_file:
        log_file.write("".join(data_lines))

@app.route('/login',methods=['POST','GET'])
def login():
    col = db.user_log
    arguments = request.args
    username = arguments['username']
    password = arguments['password']
    print(username,password)
    x  = col.find_one({'username':username,'password':password})
    print(x)
    if x :
        return json.dumps({'found':1}),200
    else:
        return json.dumps({'found':0}),200

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

@app.route('/addNote', methods=['POST', 'GET'])
def addNote():
    arguments = request.args
    searchstring = arguments['searchString']
    notestring = str(arguments['note']).strip()
    if notestring=="":
        return '',203
    keyword = searchstring.split()[0]
    collection = db.notes
    result = collection.find_one({"keyword": keyword})
    search_date_time = datetime.now()
    if result is None:
        collection.insert_one({"keyword": keyword, "Notes": [{"note":notestring, "date_time": str(search_date_time)}]})
    else:
        noteslist = result["Notes"]
        new_entry = {"note": notestring, "date_time": str(search_date_time)}
        noteslist.append(new_entry)
        collection.update({"keyword": keyword},{"keyword": keyword, "Notes": noteslist})
    return '', 204


@app.route('/findNotes', methods=['POST', 'GET'])
def findNotes():
    arguments = request.args
    searchstring = arguments['searchString']
    keyword = searchstring.split()[0]
    collection = db.notes
    result = collection.find_one({"keyword": keyword})
    if result is None:
        return '', 204
    else:
        return json.dumps(result["Notes"])

@app.route('/search', methods=['POST', 'GET'])
def search():
    arguments = request.args
    searchstring = arguments['searchString']
    update_search_log(searchstring)
    search_expr = re.compile(f".{searchstring}.", re.I)
    results = collection.find({"$or": [{"author": search_expr}, {"title": search_expr}]})
    json_docs = [json.dumps(doc, default=json_util.default) for doc in results]
    # print(json_docs)
    catalogue_service_response = requests.post(base_url + str(":5000/catalogue-service"),
                                               json={'data': json.dumps(json_docs)})
    print(catalogue_service_response)
    # make a request to catalogue api
    return json.dumps(json_docs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
