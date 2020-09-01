from flask import Flask, render_template, url_for, request, redirect
import requests
import logging
from time import sleep
from sys import stdout  #for dynamic printing in console
import json
import urllib.parse
import pyfiglet #for banners

# create logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log/webApp.log", level = logging.DEBUG, format=LOG_FORMAT, filemode = 'w')
logger = logging.getLogger()

app = Flask(__name__)
databaseMS_URL = "http://0.0.0.0:5001"

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
def years():
    try:
        r = requests.get(url = databaseMS_URL + "/years")
        r_url = databaseMS_URL + "/years"
        print(f"date_url={r_url}")
    except:
        logger.error("Could not get HTTP response from databaseMS.")
        return "Could not get HTTP response from databaseMS."
    else:
        logger.info("Successfully obtained HTTP response from databaseMS about occuring years.")
        occuringYears = json.loads(r.content)
        return render_template("years.html", years = occuringYears)

@app.route('/date/<int:year>')
@app.route('/date/<int:year>/<int:month>')
@app.route('/date/<int:year>/<int:month>/<int:day>')
def date(year=None, month=None, day=None):
    # return f"Showing months for year {year}"
    try:
        print("Im here!")
        args = {"year": year, "month": month}
        print(f"My args are: year: {year}, month: {month} \n")

        #Showing available months in a year
        if year!=None and month==None and day==None:
            #Try to get a response from dbMS
            try:
                newUrl = databaseMS_URL + "/showMonthsFor" + "/" + str(year)
                print(f"year: {year}")
                print(f"(1)Making request at r={newUrl}")
                r = requests.get(url = databaseMS_URL + "/showMonthsFor" + "/" + str(year))
                print(f"r: {r}")
            except:
                msg = "Could not get HTTP response from databaseMS about occuring months in a yearasikdg."
                logger.error(msg)
                return msg
            else:
                # return r_display
                msg = "Successfully obtained HTTP response from databaseMS about occuring months in a year."
                logger.info(msg)
                occuringMonths = json.loads(r.content)
                print(f"My response from dbMS: {occuringMonths}\n")
                return render_template("months.html", year = year, months = occuringMonths)


        #Showing available days in a month
        elif year!=None and month!=None and day==None:
            print(2)
        #Showing measurements from specific day
        elif year!=None and month!=None and day!=None:
            print(3)
        else:
            print(4)

        args_encoded = urllib.parse.urlencode(args)
        print(f"args encoded: {args_encoded}")
        url = databaseMS_URL + "?" + args_encoded
        print(url)
        return url
        # r = requests.get(url = url)

        # if (year != None) and (month == day == None):
        #     args = {"year": year}
        #     url = databaseMS_URL + "?" + urllib.urlencode(args)
        #     r = requests.get(url = url)
        # elif year != None and month != None and day == None:
        #     r = "Nie ma tylko dnia"
        # elif year != None and month != None and day != None:
        #     r = "Jest dzien, mc, rok"
        # else:
        #     r = "Żaden z typów daty nie podany w prawidłowej formie."


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

@app.route('/login')
@app.route('/login/<name>')
def loginPage(name=None):
    try:
        return render_template('login.html', name=name)
    except:
        return 'Could not load login page.'

if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Welcome to EnvSens!")
    # print("webApp: Waiting until the database is up...")
    # sleep(2)
    print("Setting up server at: {}".format("http://0.0.0.0:5000/"))
    print(ascii_banner)
    app.run(debug=True, host='0.0.0.0', port=5000)  #ascii(w)=119
