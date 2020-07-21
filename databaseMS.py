from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Measurement(db.Model):
    id =            db.Column(db.Integer, primary_key=True, nullable=False)
    temperature =   db.Column(db.Float, nullable=False, default=20)
    humidity =      db.Column(db.Float, nullable=False, default=20)
    timestamp =      db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Measurment %r>' % self.id

@app.route('/receiveMeasurement', methods=['POST'])
def result():
    if request.method == 'POST':
        temp = request.form['temperature']
        hum = request.form['humidity']
        timestamp = request.form['timestamp']

        new_measurement = Measurement(temperature=temp, humidity=hum, timestamp=timestamp)
        try:
            db.session.add(new_measurment)
            db.session.commit()
            return 'Measurement added successfully!'
        except:
            return 'There was an issue adding a measurment.'

if __name__ == "__main__":
    app.run(debug=True)


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