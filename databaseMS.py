from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
import time

#create logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log/databaseMS.log", level = logging.DEBUG, format=LOG_FORMAT, filemode = 'w')
logger = logging.getLogger()

#configure server and db
app = Flask(__name__)
dbFileName = "test" #w/ an extension
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + dbFileName + ".db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

def checkDb(db):
    db.create_all()

class Measurement(db.Model):
    #id as PK is automatically set has autoincrement=True
    id =            db.Column(db.Integer, primary_key=True, nullable=False)
    temperature =   db.Column(db.Float, nullable=False, default=20)
    humidity =      db.Column(db.Float, nullable=False, default=20)
    timestamp =     db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Measurement: id=%r t=%f h=%f ts=%a>' % (self.id, self.temperature, self.humidity, self.timestamp)



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
            logger.info("Frame successfully commited to the db")
            # return 'Stomething.'
        except:
            logger.error("Measurement failed to be inserted to the db.")
            return 'There was an issue adding a measurment.'
        else:
            logger.info("Measurement successfully inserted to the db.")
            return 'Measurement successfully inserted to the db.'

@app.route('/getAllMeasurements', methods=['GET'])
def getAllMeasurements():
    if request.method == 'GET':
        # return "Zwracam pomiary..."
        try:
            measurements = Measurement.query.order_by(Measurement.timestamp).all()
            measurements = Measurement.query.all()
            print("type(measurements[1]): {}".format(type(measurements[1])))
        except:
            logger.error("Database is temporarily in a lockdown mode.")
            return "Database is temporarily in a lockdown mode."
        else:
            logger.info("Successfully sent HTTP message to webApp.")
        return render_template('index.html', measurements=measurements)


if __name__ == "__main__":
    checkDb(db)
    app.run(debug=True, host='127.0.0.100', port=42000)


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
1) source /venv/bin/activate    or      venv
2) python
3) from databaseMS import Measurement, db
4) db.create_all()
5) Measurement.query.all()
6) exit()
"""