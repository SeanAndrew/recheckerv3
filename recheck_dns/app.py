import copy

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import datetime
import json
import requests
import dns.resolver
from pymongo import MongoClient
#from elasticsearch import Elasticsearch, RequestsHttpConnection

app = FastAPI()

# es = Elasticsearch(['https://kibana.rechecker.local:443'])
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
def dns_checker(domain: str):
    print('I check DNS status')
    dns_checker_response = {
        "domain": f"{domain}",
        "timestamp": f"{time}"
    }

    try:
        call = dns.resolver.resolve(domain, 'A')
        print("Upserting data")
        #upsert
        upsert_result = status_table.update_one({"domain": f"{domain}"}, {"$set": dns_checker_response}, upsert=True)
        # TODO should rework this for loop as i'm 99% sure it's not required
        for ipval in call:
            json_ify = jsonable_encoder(dns_checker_response)
            print(json.dumps(dns_checker_response), flush=True)
            return JSONResponse(content=json_ify)
    except dns.resolver.NXDOMAIN:
        #res = es.index(index=index, body=dns_check_response)
        #print(res['result'], flush=True)
        dns_checker_response["error_message"] = "not found"
        print("Upserting data")
        #upsert
        upsert_result = status_table.update_one({"domain": f"{domain}"}, {"$set": dns_checker_response}, upsert=True)
        json_ify = jsonable_encoder(dns_checker_response)
        print(json.dumps(dns_checker_response), flush=True)
        return JSONResponse(content=json_ify)
    except dns.resolver.NoAnswer:
        #res = es.index(index=index, body=dns_check_response)
        #print(res['result'], flush=True)
        dns_checker_response["error_message"] = "no reply"
        #upsert
        print("Upserting data")
        upsert_result = status_table.update_one({"domain": f"{domain}"}, {"$set": dns_checker_response}, upsert=True)
        json_ify = jsonable_encoder(dns_checker_response)
        print(json.dumps(dns_checker_response), flush=True)
        return JSONResponse(content=json_ify)
    except dns.exception.Timeout:
        #res = es.index(index=index, body=dns_check_response)
        #print(res['result'], flush=True)
        dns_checker_response["error_message"] = "timeout"
        #upsert
        print("Upserting data")
        upsert_result = status_table.update_one({"domain": f"{domain}"}, {"$set": dns_checker_response}, upsert=True)
        json_ify = jsonable_encoder(dns_checker_response)
        print(json.dumps(dns_checker_response), flush=True)
        return JSONResponse(content=json_ify)