from flask import Flask, render_template, url_for, request, redirect
import requests
import logging
from time import sleep
from sys import stdout  #for dynamic printing in console
import json
import urllib


# create logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log/webApp.log", level = logging.DEBUG, format=LOG_FORMAT, filemode = 'w')
logger = logging.getLogger()

app = Flask(__name__)
databaseMS_URL = "http://127.0.0.100:42000"

"""Prints countdown"""
# def countDown(n):
#     for i in range(n,0,-1):
#         stdout.write("\r%d... " % i)
#         stdout.flush()
#         sleep(1)
#     stdout.write("\n") # move the cursor to the next line


@app.route('/', methods=['GET'])
def index():
    try:
        r = requests.get(url = databaseMS_URL + "/getAllMeasurements")
    except:
        logger.error("Could not get HTTP response from databaseMS.")
        return "Could not get HTTP response from databaseMS."
    else:
        logger.info("Successfully obtained HTTP response from databaseMS.")
        json_string = r.content
        measurements = json.loads(json_string)
        return render_template('index.html', measurements=measurements)

@app.route('/years')
def years():
    try:
        r = requests.get(url = databaseMS_URL + "/years")
    except:
        logger.error("Could not get HTTP response from databaseMS.")
        return "Could not get HTTP response from databaseMS."
    else:
        logger.info("Successfully obtained HTTP response from databaseMS about occuring years.")
        occuringYears = json.loads(r.content)
        return render_template("years.html", years = occuringYears)

@app.route('/showMonthsFor/<int:year>')
def showMonthsFor(year):
    # return f"Showing months for year {year}"
    try:
        args = {"year": year}
        url = databaseMS_URL + "?" + urllib.urlencode(args)
        r = requests.get(url = url)
    except:
        error = "Could not get HTTP response from databaseMS about occuring months in a year."
        logger.error(error)
        return error
    else:
        info = "Successfully obtained HTTP response from databaseMS about occuring months in a year."
        logger.info(info)
        # occuringMonths = json.loads(r.content)
        # return f"Got months for year {year}"
        return r
        # return render_template("years.html", years = occuringYears)

@app.route('/showSomething')
def showSomething():
    return "Something"

@app.route('/yoki')
def yoki():
    try:
        r = requests.get(url = databaseMS_URL + "/yoki")
    except:
        return "Yoki cannot work"
    else:
        return r.content

@app.route('/login')
@app.route('/login/<name>')
def loginPage(name=None):
    try:
        return render_template('login.html', name=name)
    except:
        return 'Could not load login page.'

if __name__ == "__main__":
    print("webApp: Waiting until the database is up...")
    sleep(5)
    print("Setting up server at: {}".format("http://127.0.0.1:5000/"))
    app.run(debug=True, host='0.0.0.0', port=5000)  #ascii(w)=119
