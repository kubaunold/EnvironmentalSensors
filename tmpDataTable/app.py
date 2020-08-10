from flask import Flask, render_template, url_for, request, redirect
import requests
import json
app = Flask(__name__)



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