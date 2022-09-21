from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pymongo
from pymongo import MongoClient
#import requests
#from urllib.parse import urlparse

app = FastAPI()

@app.post("/{domain}")
# TODO rework to match FastAPI type Var use
def update_db(domain: str):
    print("I delete old entries in MongoDB from MariaDB")
    # raw_json = requests.get_json
    try:
        client = MongoClient("mongodb+srv://user:password@cluster.id.mongodb.net/host?retryWrites=true&w=majority")
        db = client.endpoints
        collection = db.sites
        # site = urlparse(raw_json("domain"))
        #print(domain, flush=True)
        delete_result = collection.inventory.deleteone({"domain": domain})
        print(delete_result.raw_result, flush=True)
        json_ify = jsonable_encoder(delete_result)
        return JSONResponse(content=json_ify)
    except pymongo.errors.ConfigurationError as err:
        print('Please check the syntax of your cluster in MongoClient', flush=True)
        json_ify = jsonable_encoder(err)
        return JSONResponse(content=json_ify)
    except pymongo.errors.InvalidURI as err:
        print('Please check the syntax of your URI in MongoClient', flush=True)
        json_ify = jsonable_encoder(err)
        return JSONResponse(content=json_ify)
    except pymongo.errors.OperationFailure as err:
        print('Check your username and password', flush=True)
        json_ify = jsonable_encoder(err)
        return JSONResponse(content=json_ify)
    # return jsonify({"entry removed": "ok"}), 200