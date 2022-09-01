from typing import List
import requests
from flask import Flask, render_template, request
from unidecode import unidecode


URL = "http://transfer.ttc.com.ge:8080/otp/routers/ttc/stopArrivalTimes"

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index() -> str:
    if request.method == 'POST':
        if request.form.get('stop_id') and request.form.get('get_schedule'):
            if request.form.get('stop_id').isdigit():
                return render_template('arrival.html', items=get_schedule(request.form.get('stop_id')))
    return render_template('index.html')

def get_schedule(stop_id: str) -> List:
    r = requests.get(f"{URL}?stopId={stop_id}")
    schedule = []
    print(r.json())
    for bus in r.json()['ArrivalTime']:
        schedule.append(
            {
                'bus': bus['RouteNumber'],
                'time': bus['ArrivalTime'],
                'destination':unidecode(bus['DestinationStopName'])
            }
        )
    print(schedule)
    return schedule

@app.route('/about', methods=["GET"])
def about() -> str:
  return render_template('about.html')
