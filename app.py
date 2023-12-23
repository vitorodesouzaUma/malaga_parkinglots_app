from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import logging, requests, os, json
from utils.data_fetching import fetch_parking_data

# Open Flask and Scheduler
app = Flask(__name__)
scheduler = BackgroundScheduler()

# Log parameters
logging.basicConfig(filename='parkinglots.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Define a global variable to store parking lot data
parking_data = []

def fetch_data():
    global parking_data
    parking_data = fetch_parking_data()

# Schedule the data fetch every minute
scheduler.add_job(func=fetch_parking_data, trigger="interval", minutes=1)
scheduler.start()


# Route to render the map and table
@app.route('/')
def index():
    return render_template('index.html', parking_data=parking_data)

@app.route('/map')
def map():
    return json.dumps(parking_data[0]['parkinglots'])

if __name__ == '__main__':

    # Start the Flask app
    fetch_data()
    app.run(debug=True)