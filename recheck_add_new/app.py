from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
import pymongo
from pymongo import MongoClient
import requests
from urllib.parse import urlparse

app = FastAPI()

@app.get("/{domain}")
# TODO rework this to fit FastAPI vars
def update_db(domain: str):
    print("I update MongoDB from MySql")
    # domains = json.loads(requests.get("http://recheck-query-db-service:5000").text)
    # for domain in domains:
    try:
        client = MongoClient("mongodb+srv://user:password@cluster.id.mongodb.net/host?retryWrites=true&w=majority")
        db = client.endpoints
        collection = db.sites
        # site = urlparse(domain["domain"])
        print(domain, flush=True)
        doc = {"domain": domain.netloc}
        print(doc, flush=True)
        upsert_result = collection.update_one( doc, { "$set": doc }, upsert=True )
        print(upsert_result.raw_result, flush=True)
        json_ify = jsonable_encoder(upsert_result)
        return JSONResponse(content=json_ify)
    except pymongo.errors.ConfigurationError as err:
        print('Please check the syntax of your cluster in MongoClient', flush=True)
        json_ify = jsonable_encoder(err)
        return JSONResponse(content=json_ify)
    except pymongo.errors.InvalidURI as err:
        print('Please check the syntax of your URI in MongoClient', flush=True)
        json_ify = jsonable_encoder(err)
        return JSONResponse(content=json_ify)
        # in case username or password is incorrect
    except pymongo.errors.OperationFailure as err:
        print('Check your username and password', flush=True)
        json_ify = jsonable_encoder(err)
        return JSONResponse(content=json_ify)
