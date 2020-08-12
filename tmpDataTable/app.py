from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def hello_world():    
    try:
        r = requests.get(url = "http://127.0.0.1:5002/")
    except:
        return "Could not get HTTP response from generator."
    else:
        bigJson = r.content
        y = json.loads(bigJson)
        # ___here prepare measurements___
        return render_template('index.html', measurements=y)

@app.route('/login')
@app.route('/login/<name>')
def loginPage(name=None):
    try:
        return render_template('login.html', name=name)
    except:
        return 'Could not load login page.'

@app.route('/name')
@app.route('/name/<namy>')
def sayHello(namy="Alen"):
    return f"Hello, {namy}"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/years')
def years():
    years = [2019, 2020]
    try:
        return render_template('years.html', years=years)
    except:
        return 'Could not load "years" page.'

@app.route('/backs')
def show_all():
   return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)



"""
    #r: <Response [200]>
    #type(r): <class 'requests.models.Response'>
    r = requests.get(url = "http://127.0.0.1:5002/")
    #type(r.content): <class 'bytes'>
    # type(my_json): <class 'str'>
    my_json = r.content.decode('utf8')
    return my_json
"""

""" Create new database
sqlite3 login.db
sqlite>     .tables //checks for active tables (should return nothing if empty)
sqlite>     .exit
"""