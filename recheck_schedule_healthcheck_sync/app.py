import json
import requests
# TODO test this function to print domain in for loop to confirm it's returning a list of domains
def healthcheck_sync():
    print('I schedule the healthcheck')
    response = requests.get("http://rechecker-endpoint:8080/")
    domains = json.loads(response.text)
    for domain in json.loads(domains[0]['body']):
        print(domain)
        try:
            requests.post("http://rechecker-http:8080/" + domain)
            requests.post("http://rechecker-dns:8080/" + domain)
        except:
            post_failed = ({
                    "_source": {
                        "message": f"{domain}",
                        "status": "failed to post"
                    }
                })
            print(json.dump(post_failed))
            pass
    print('ok', flush=True)
healthcheck_sync()