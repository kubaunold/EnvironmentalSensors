"""
[TODO]
- 


[DONE]
"""

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
import logging
from time import sleep
from sys import stdout  # for dynamic printing in console
import json
import urllib.parse
import pyfiglet  # for banners

# create logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="log/webApp.log", level=logging.DEBUG, format=LOG_FORMAT, filemode='w')
logger = logging.getLogger()

# app config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + "login" + ".db"
app.config['SECRET_KEY'] = "thisissecret"

# db and login config
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

databaseMS_URL = "http://0.0.0.0:5001"

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

 
@app.route('/', methods=['GET'])
@login_required
def index():
    """ This function is triggered when we open the homepage
    """
    try:
        r = requests.get(url=databaseMS_URL + "/getAllMeasurements")
        r_url = databaseMS_URL + "/getAllMeasurements"
        print(f"(0)Making request at r={r_url}")
    except:
        logger.error("Could not get HTTP response from databaseMS.")
        return "Could not get HTTP response from databaseMS."
    else:
        logger.info("Successfully obtained HTTP response from databaseMS.")
        json_string = r.content
        measurements = json.loads(json_string)
        return render_template('index.html', measurements=measurements)


@app.route('/date')
@login_required
def years():
    try:
        r = requests.get(url=databaseMS_URL + "/years")
        r_url = databaseMS_URL + "/years"
        print(f"date_url={r_url}")
    except:
        logger.error("Could not get HTTP response from databaseMS.")
        return "Could not get HTTP response from databaseMS."
    else:
        logger.info(
            "Successfully obtained HTTP response from databaseMS about occuring years.")
        occuringYears = json.loads(r.content)
        return render_template("years.html", years=occuringYears)


@app.route('/date/<int:year>')
@app.route('/date/<int:year>/<int:month>')
@app.route('/date/<int:year>/<int:month>/<int:day>')
@login_required
def date(year=None, month=None, day=None):
    args = {"year": year, "month": month, "day": day}
    print(f"My args are: year: {year}, month: {month}, day: {day} \n")

    print("Im here!")
    # Showing available months in a year
    if year != None and month == None and day == None:
        # Try to get a response from dbMS
        try:
            newUrl = databaseMS_URL + "/showMonthsFor" + "/" + str(year)
            print(f"year: {year}")
            print(f"(1)Making request at r={newUrl}")
            r = requests.get(url=databaseMS_URL + "/showMonthsFor" + "/" + str(year))
            print(f"r: {r}")
        except:
            msg = "Could not get HTTP response from databaseMS about occuring months in a yearasikdg."
            logger.error(msg)
            return msg
        else:
            # return r_display
            msg = "Successfully obtained HTTP response from databaseMS about occuring months in a year wfpj."
            logger.info(msg)
            occuringMonths = json.loads(r.content)
            print(f"My response from dbMS: {occuringMonths}\n")
            return render_template("months.html", year=year, months=occuringMonths)

    # Showing available days in a month
    elif year != None and month != None and day == None:
        try:
            url = databaseMS_URL + "/showDaysFor" + \
                "/" + str(year) + "/" + str(month)
            print(f"url: {url}")
            r = requests.get(url=url)            
        except:
            msg = "Could not get HTTP response from databaseMS about occuring days in a month."
            logger.error(msg)
            return msg
        else:
            # return r_display
            msg = "Successfully obtained HTTP response from databaseMS about occuring days in a month."
            logger.info(msg)
            occuringDays = json.loads(r.content)
            print(f"My response from dbMS: {occuringDays}\n")
            return render_template("days.html", year=year, month=month, days=occuringDays)

    # Showing measurements from specific day
    elif year != None and month != None and day != None:
        try:
            url = databaseMS_URL + "/showMeasurementsFor" + \
                "/" + str(year) + "/" + str(month) + "/" + str(day)
            print(f"url: {url}")
            r = requests.get(url=url)
        except:
            msg = "Could not get response from databaseMS about measurements on a specific day."
            logger.error(msg)
            return msg
        else:
            info = "Successfully obtained response from databaseMS about measurements on a specific day."
            logger.info(info)
            json_string = r.content
            measurements = json.loads(json_string)
            return render_template('index.html', measurements=measurements)
    
    else:
        print(4)

    args_encoded = urllib.parse.urlencode(args)
    print(f"args encoded: {args_encoded}")
    url = databaseMS_URL + "?" + args_encoded
    print(url)
    
    return url


@app.route('/login')
@app.route('/login/<name>')
def loginPage(name=None):
    # try:
    #     return render_template('login.html', name=name)
    # except:
    #     return 'Could not load login page.'
    user = User.query.filter_by(username='Kuba').first()
    login_user(user)
    return "Kuba, you are now logged in!"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "You are now logged out!"

def main():
    ascii_banner = pyfiglet.figlet_format("Welcome to EnvSens!")
    # print("webApp: Waiting until the database is up...")
    # sleep(2)
    print("Setting up server webServer at: {}".format("http://0.0.0.0:5000/"))
    print(ascii_banner)
    app.run(debug=True, host='0.0.0.0', port=5000)  # ascii(w)=119


if __name__ == "__main__":
    main()



""" CREATE NEW TABLE
python
>>> from webApp import db
>>> db.create_all()
>>> exit()
"""
""" SEE THE CREATION
sqlite3 login.db
>>> .tables
>>> .exit
"""
""" ADD NEW USER
python
>>> from webApp import db, User
>>> kuba = User(username="Kuba")
>>> db.session.add(kuba)
>>> db.session.commit()

>>> results = User.query.all()
>>> results[0].username
>>> exit()
"""