from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Measurement(db.Model):
    id =            db.Column(db.Integer, primary_key=True, nullable=False)
    temperature =   db.Column(db.Integer, nullable=False, default=20)
    humidity =      db.Column(db.Integer, nullable=False, default=20)
    datetime =      db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Measurment %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        measurment_temp = request.form['temp']
        measurment_hum = request.form['hum']
        new_measurment = Measurment(temperature = measurment_temp, humidity=measurment_hum)
        try:
            db.session.add(new_measurment)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your measurment form the webpage'

    else:
        measurments = Measurment.query.order_by(Measurment.time).all()
        measurments = Measurment.query.all()
        return render_template('index.html', measurments=measurments)


@app.route('/delete/<int:id>')
def delete(id):
    measurment_to_delete = Measurment.query.get_or_404(id)

    try:
        db.session.delete(measurment_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that measurment'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    measurment = Measurment.query.get_or_404(id)

    if request.method == 'POST':
        measurment.temperature = request.form['temp']
        measurment.humidity = request.form['hum']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your measurment'

    else:
        return render_template('update.html', measurment=measurment)

@app.route('/receiveMeasurement', methods=['POST'])
def result():
    # print(request.form['foo']) # should display 'bar'
    measurement_temp = request.form['temperature']
    measurement_hum = request.form['humidity']
    
    new_measurment = Measurment(temperature = measurment_temp, humidity=measurment_hum)
    try:
        db.session.add(new_measurment)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your measurment drom another script'
    

if __name__ == "__main__":
    app.run(debug=True)


"""
HOW TO RESET DB?
1) ..\Envs\py382_flask\Scripts\activate
2) sudo python
2,5) remove test.db
3) from webSensorApp2 import db
4) db.create_all()
5) exit()

voila!
"""
""" INSTALL FLASK AND SQLALCHEMY
sudo pip install flask
sudo pip install sqlalchemy
"""