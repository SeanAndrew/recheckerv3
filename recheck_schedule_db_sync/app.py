import json
import requests
def schedule_db_sync():
    print('I sync db')
    # TODO 
    #recheck_query = requests.get("http://recheck-query-db-service:5000")
    recheck_update = json.loads(requests.get("http://recheck-update-db-service:5000").text)
    print(json.dumps(recheck_update), flush=True)
    return json.dumps(recheck_update), 200
schedule_db_sync()