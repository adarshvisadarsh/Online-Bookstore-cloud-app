from flask import Flask, render_template, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
from datetime import datetime
import re
import json
#pip3 freeze > requirements.txt

aws_instance_ip = "18.213.176.85"
app = Flask(__name__)
cors = CORS(app)
client = MongoClient("mongodb://dbuser:dbpwd@" + aws_instance_ip + "/books_db")
db = client.books_db
collection = db["books"]


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
