from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)

# Define a global variable to store parking lot data
parking_data = []

def fetch_parking_data():
    global parking_data
    api_url = "https://datosabiertos.malaga.eu/recursos/aparcamientos/ocupappublicosmun/ocupappublicosmunfiware.json"
    response = requests.get(api_url)
    if response.status_code == 200:
        parking_data = response.json()
    else:
        parking_data = []

# Schedule the data fetch every minute
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_parking_data, trigger="interval", minutes=1)
scheduler.start()

# Route to render the map and table
@app.route('/')
def index():
    return render_template('index.html', parking_data=parking_data)

@app.route('/map')
def map():
    return parking_data

if __name__ == '__main__':
    # Initial fetch of data
    fetch_parking_data()

    # Start the Flask app
    app.run(debug=True)