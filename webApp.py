from flask import Flask, render_template, url_for, request, redirect
import requests
import logging

#create logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log/webApp.log", level = logging.DEBUG, format=LOG_FORMAT, filemode = 'w')
logger = logging.getLogger()

app = Flask(__name__)
databaseMS_URL = "http://127.0.0.100:42000/getAllMeasurements"

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
    app.run(debug=True, host='0.0.0.0', port=5000)  #ascii(w)=119