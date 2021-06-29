from flask import Flask, render_template, request, make_response
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
from datetime import datetime
import re
import json
import requests

base_url = "http://18.213.176.85"
aws_instance_ip = "18.213.176.85"
app = Flask(__name__)
cors = CORS(app)
client = MongoClient("mongodb://dbuser:dbpwd@" + aws_instance_ip + "/books_db")
db = client.books_db
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


@app.route('/search', methods=['POST', 'GET'])
def search():
    arguments = request.args
    searchstring = arguments['searchString']
    update_search_log(searchstring)
    search_expr = re.compile(f".{searchstring}.", re.I)
    results = collection.find({"$or": [{"author": search_expr}, {"title": search_expr}]})
    json_docs = [json.dumps(doc, default=json_util.default) for doc in results]
    # print(json_docs)
    catalogue_service_response = requests.post(base_url + str(":6000/catalogue-service"),
                                               json={'data': json.dumps(json_docs)})
    print(catalogue_service_response)
    # make a request to catalogue api
    return json.dumps(json_docs)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
