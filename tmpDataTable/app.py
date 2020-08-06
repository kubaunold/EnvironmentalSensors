from flask import Flask, render_template, url_for, request, redirect
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        r = requests.get(url = "http://127.0.0.1:5002/")
        #r = render_template('index.html')
    except:
        return "Could not get HTTP response from databaseMS."
    else:
        return r
    # return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
