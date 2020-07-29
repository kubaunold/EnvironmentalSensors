from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Measurement(db.Model):
    id =            db.Column(db.Integer, primary_key=True, nullable=False)
    temperature =   db.Column(db.Float, nullable=False, default=20)
    humidity =      db.Column(db.Float, nullable=False, default=20)
    timestamp =     db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Measurement: id=%r t=%f>' % (self.id, self.temperature)
# class Measurment(db.Model):
#     id =            db.Column(db.Integer, primary_key=True, nullable=False)
#     temperature =   db.Column(db.Integer, nullable=False, default=20)
#     humidity =      db.Column(db.Integer, nullable=False, default=20)
#     time =          db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Measurment %r>' % self.id

@app.route('/', methods=['GET'])
def index():
    # measurements = Measurement.query.order_by(Measurement.timestamp).all()
    measurements = Measurement.query.all()
    return render_template('index.html', measurements=measurements)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  #ascii(w)=119