from flask import render_template
from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient(
    host = 'mongo:27017',
    serverSelectionTimeoutMS = 3000,
    username="root",
    password="example",
)

db = client.endpoints
status_table = db.status
@app.route('/')
@app.route('/index')
def index():

    all_results = status_table.find({})
    error_domains = []
    for row in all_results:
        if len(row['error_message']) > 0:
            error_domains.append(row)

    return render_template('index.html', title='Rechecker', error_domains = error_domains)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True)