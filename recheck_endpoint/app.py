from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pymongo
from pymongo import MongoClient

app = FastAPI()

@app.get("/")
def get_endpoints():
    print('I provide a list of endpoints')
    domains = []
    try:
        #client = MongoClient("mongodb+srv://user:password@cluster.id.mongodb.net/host?retryWrites=true&w=majority")
        ### local mongodb
        client = MongoClient("mongodb://root:example@mongo:27017/")
        # .endpoints refers to the database to connect to
        db = client.endpoints
        # This for look loop iterates over each entry in the database.
        # These are json entries with name: "domain.com" key value pairs
        # .sites is the Collection in the .endpoints database
        #domains = db.sites.find()
        for site in db.sites.find():
            domains.append(site['domain'])
        json_ify = jsonable_encoder(domains)
        client.close()
        return JSONResponse(content=json_ify), 200
    # in case URI syntax is incorrect
    except pymongo.errors.ConfigurationError:
        print('Please check the syntax of your cluster in MongoClient', flush=True)
        raise HTTPException(status_code=404)
    except pymongo.errors.InvalidURI:
        print('Please check the syntax of your URI in MongoClient', flush=True)
        raise HTTPException(status_code=401)
    # # in case username or password is incorrect
    except pymongo.errors.OperationFailure:
        print('Check your username and password', flush=True)
        raise HTTPException(status_code=401)