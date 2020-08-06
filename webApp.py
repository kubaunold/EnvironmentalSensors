from flask import Flask, render_template, url_for, request, redirect
import requests
import logging
from time import sleep
from sys import stdout  #for dynamic printing in console

# create logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log/webApp.log", level = logging.DEBUG, format=LOG_FORMAT, filemode = 'w')
logger = logging.getLogger()

app = Flask(__name__)
databaseMS_URL = "http://127.0.0.100:42000/getAllMeasurements"

# def countDown(n):
#     for i in range(n,0,-1):
#         stdout.write("\r%d... " % i)
#         stdout.flush()
#         sleep(1)
#     stdout.write("\n") # move the cursor to the next line


@app.route('/', methods=['GET'])
def index():
    try:
        r = requests.get(url = databaseMS_URL)
    except:
        logger.error("Could not get HTTP response from databaseMS.")
        return "Could not get HTTP response from databaseMS."
    else:
        logger.info("Successfully obtained HTTP response from databaseMS.")
        return r.content

if __name__ == "__main__":
    print("webApp: Waiting until the database is up...")
    sleep(5)
    print("Setting up server at: {}".format("http://127.0.0.1:5000/"))
    app.run(debug=True, host='0.0.0.0', port=5000)  #ascii(w)=119