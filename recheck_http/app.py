from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
# from elasticsearch import Elasticsearch, RequestsHttpConnection
import datetime
import json
import requests
from pymongo import MongoClient


app = FastAPI()
# es = Elasticsearch(['https://kibana.rechecker.local:443'])
# # set elastic index
# index = ("rechecker-" + str(date))
time = datetime.datetime.now()
date = datetime.date.today()


client = MongoClient(
    host = 'mongo:27017',
    serverSelectionTimeoutMS = 3000,
    username="root",
    password="example",
)

db = client.endpoints
status_table = db.status


@app.post("/{domain}")
async def http_checker(domain: str):
    print('I check http status')
    http_checker_response = {
                "domain": f"{domain}",
                "timestamp": f"{time}"
    }
    try:
        requests.get('http://' + domain, timeout=1)
        # code = str(call.status_code)
        # http_checker_response["status_code"] = code
        http_checker_response["error_message"] = ''
        print("Upserting data")
        #upsert
        upsert_result = status_table.update_one({"domain": f"{domain}"}, {"$set": http_checker_response}, upsert=True)

        json_ify = jsonable_encoder(http_checker_response)
        print(json.dumps(http_checker_response), flush=True)
        # res = es.index(index=index, body=http_checker_response)
        #     # print(res['result'], flush=True)
        return JSONResponse(content=json_ify)
    except requests.ConnectionError:
        code = 500
        print("Upserting data")
        # res = es.index(index=index, body=http_checker_response)
        # print(res['result'], flush=True)
        http_checker_response["status_code"] = code
        http_checker_response["error_message"] = "connection error"
        #upsert
        upsert_result = status_table.update_one({"domain": f"{domain}"}, {"$set": http_checker_response}, upsert=True)
        json_ify = jsonable_encoder(http_checker_response)
        print(json.dumps(http_checker_response), flush=True)
        return JSONResponse(content=json_ify)
    except requests.exceptions.ReadTimeout:
        code = 500
        # res = es.index(index=index, body=http_checker_response)
        # print(res['result'], flush=True)
        http_checker_response["status_code"] = code
        http_checker_response["error_message"] = "read timeout"
        print("Upserting data")
        #upsert
        upsert_result = status_table.update_one({"domain": f"{domain}"}, {"$set": http_checker_response}, upsert=True)
        json_ify = jsonable_encoder(http_checker_response)
        print(json.dumps(http_checker_response), flush=True)
        return JSONResponse(content=json_ify)