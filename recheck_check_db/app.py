
# TODO create new api function that checks for changes in mysql vs mongodb and ships those changes to delete_old

from fastapi import FastAPI
import pymongo
from pymongo import MongoClient
import requests
from urllib.parse import urlparse

app = FastAPI()

@app.post("/")
# TODO rework to match FastAPI type Var use
def update_db():
    print("I delete old entries in MongoDB from MariaDB")
    raw_json = requests.get_json
    try:
        client = MongoClient("mongodb+srv://user:password@cluster.id.mongodb.net/host?retryWrites=true&w=majority")
        db = client.endpoints
        collection = db.sites
        site = urlparse(raw_json("domain"))
        print(site, flush=True)
        delete_result = collection.inventory.deleteone( { "domain": site } )
        print(delete_result.raw_result, flush=True)
    except pymongo.errors.ConfigurationError:
        print('Please check the syntax of your cluster in MongoClient', flush=True)
        # TODO abort is a flask module
        return abort(404)
    except pymongo.errors.InvalidURI:
        print('Please check the syntax of your URI in MongoClient', flush=True)
        # TODO abort is a flask module
        return abort(401)
        # in case username or password is incorrect
    except pymongo.errors.OperationFailure:
        print('Check your username and password', flush=True)
        # TODO abort is a flask module
        return abort(401)
    return jsonify({"entry removed": "ok"}), 200
