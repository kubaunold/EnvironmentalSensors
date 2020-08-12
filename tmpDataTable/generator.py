from flask import Flask
import json
import random
from datetime import datetime, timedelta

app = Flask(__name__)

def gen_datetime(min_year=1900, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

def generate(i):
    id = i
    temp = random.uniform(-10, 40)
    hum = random.uniform(30, 90)
    timestamp = str(gen_datetime())
    return {'id': id, 'temperature': temp, 'humidity': hum, 'timestamp': timestamp}
    # return {'id': id, 'temperature': temp, 'humidity': hum}

@app.route('/')
def hello_world():
    # meas1 = {'id': 1, 'temperature': 13.5, 'humidity': 43.8, 'timestamp': '2020-08-06 11:58:15.924420'}
    d = []
    for i in range(3600):
        newMeasurement = generate(i)
        d.append(newMeasurement)
    # print("Type of d: {}".format(type(d)))
    # print("Type of json.dumps(d): {}".format(type(json.dumps(d))))
    result = json.dumps(d)
    print("result: {}".format(result))
    print("Type of result: {}".format(type(result)))

    return result

@app.route('/franek')
def show_all():
    return "All"

if __name__ == "__main__":
    #will run at http://127.0.0.1:5002/
    app.run(debug=True, host='0.0.0.0', port=5002)  
