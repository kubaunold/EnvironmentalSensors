from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
import time
import json

#create logger
# LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
# logging.basicConfig(filename = "log/databaseMS.log", level = logging.DEBUG, format=LOG_FORMAT, filemode = 'w')
# logger = logging.getLogger()

#configure server and db
app = Flask(__name__)
dbFileName = "test" #w/ an extension
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + dbFileName + ".db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

def checkDb(db):
    db.create_all()

class Measurement(db.Model):
    # id as PK is automatically set has autoincrement=True
    id =            db.Column(db.Integer, primary_key=True, nullable=False)
    temperature =   db.Column(db.Float, nullable=False, default=20)
    humidity =      db.Column(db.Float, nullable=False, default=20)
    timestamp =     db.Column(db.DateTime, default=datetime.utcnow)

    # Needed for json compression
    def dump(self):
        return {'id': self.id,
                'temperature': self.temperature,
                'humidity': self.humidity,
                'timestamp': self.timestamp}

    # Returns printable representation of an object
    def __repr__(self):
        return '<Measurement: id=%r t=%f h=%f ts=%a>' % (self.id, self.temperature, self.humidity, self.timestamp)

@app.route('/', methods=['GET'])
def index():
    return "Hello, it's dbMS homepage."

@app.route('/insertMeasurement', methods=['POST'])
def result():
    if request.method == 'POST':
        temp = request.form['temperature']
        # print("Temperature = ", temp)
        hum = request.form['humidity']
        # print("Humidity = ", hum)
        mes = Measurement(temperature=temp, humidity=hum)

        timestampStr = request.form['timestamp']
        timeStampDateTimeObj = datetime.strptime(timestampStr, '%Y-%m-%d %H:%M:%S.%f')
        # print("Timestamp = ", timeStampDateTimeObj, "tsFormat: ", type(timeStampDateTimeObj))
        mes = Measurement(temperature=temp, humidity=hum, timestamp=timeStampDateTimeObj)

        try:
            db.session.add(mes)
            db.session.commit()
            # logger.info("Frame successfully commited to the db")
        except:
            # logger.error("Measurement failed to be inserted to the db.")
            return 'There was an issue adding a measurment.'
        else:
            # logger.info("Measurement successfully inserted to the db.")
            return 'Measurement successfully inserted to the db.'

@app.route('/getAllMeasurements', methods=['GET'])
def getAllMeasurements():
    if request.method == 'GET':
        try:
            measurements = Measurement.query.order_by(Measurement.timestamp).all()
            measurements = Measurement.query.all()
            # print("type(measurements[1]): {}".format(type(measurements[1])))
        except:
            # logger.error("Database is temporarily in a lockdown mode.")
            return "Database is temporarily in a lockdown mode."
        else:
            # logger.info("Successfully sent HTTP message to webApp.")
            json_string = json.dumps([o.dump() for o in measurements], indent=4, sort_keys=True, default=str)   #needed for date serialization
            return json_string

@app.route('/years')
def years():
    occuringYears = []
    try:
        minYear = Measurement.query.order_by(Measurement.timestamp.asc()).first().timestamp.year
        maxYear = Measurement.query.order_by(Measurement.timestamp.desc()).first().timestamp.year
        # print(minYear, maxYear)
        for i in range(minYear, maxYear + 1):
            currentYearResponse = Measurement.query.filter(Measurement.timestamp.startswith(str(i))).first()
            if currentYearResponse != None:
                occuringYears+=[i]
        # print(f"occuringYears: {occuringYears}")
    except:
        return 'Could not load "years" page. Bzzz'
    else:
        # logger.info("Successfully obtained occuring years.")
        return json.dumps(occuringYears)

@app.route('/showMonthsFor/<int:year>')
def showMonthsFor(year=None):
    occuringMonths = []
    print("box")
    try:
        for month in range(1, 12 + 1):
            print("fox")
            print(f"year: {year}")
            print(f"month: {month}")
            curMonthInStringFormat = datetime(int(year), month, 1).strftime("%Y-%m")    #day's required but here unnecessary
            print("beaver")
                
            print(f"curMonthInStringFormat: {curMonthInStringFormat}")
            curMonthResponse = Measurement.query.filter(Measurement.timestamp.startswith(curMonthInStringFormat + "%")).first()
            print(f"curMonthResponse: {curMonthResponse}")
            if curMonthResponse != None:
                occuringMonths+=[month]
        print(f"occuringMonths: {occuringMonths}")
    except:
        return 'Could not load "years" page. Bzzz'
    else:
        # logger.info("Successfully obtained occuring years.")
        return json.dumps(occuringMonths)

if __name__ == "__main__":
    checkDb(db)
    # app.run(debug=True, host='127.0.0.1', port=6000)
    print("Setting up server at: {}".format("http://0.0.0.0:5001/"))
    app.run(debug=True, host='0.0.0.0', port=5001)    #it'll make my server externally visible

""" HOW TO RESET DB?
1) source /venv/bin/activate
1,5) rm test.db
2) python
3) from databaseMS import db
4) db.create_all()
5) exit()
"""
""" INSTALL FLASK AND SQLALCHEMY
pip install flask  //bez sudo! inaczej zainstaluje dla roota te package, nie dla mojego uzytkownika `pi`
pip install flask-sqlalchemy
pip install numpy
"""
""" HOW TO LOOK INSIDE DB?
source /venv/bin/activate    #venv (alternatively)
python
from databaseMS import Measurement, db
db.create_all()
Measurement.query.all()
exit()
"""
""" More complex queries
Measurement.query.filter_by(id=5862).all()
Measurement.query.filter_by(id=5862).first()
Measurement.query.filter_by(id=586215).first_or_404(description='There is no data with {}'.format(15))
Measurement.query.order_by(Measurement.timestamp.desc()).first()

dt = Measurement.query.filter(Measurement.timestamp.like("2020-07-29 13:43%")).first()
print(dt.timestamp)
"""