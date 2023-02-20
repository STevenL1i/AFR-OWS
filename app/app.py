import json
from flask import *
from gevent import pywsgi

import authenticator as auth

app = Flask("__name__")

@app.after_request
def cors(environ):
    environ.headers["Access-Control-Allow-Origin"] = "*"
    environ.headers["Access-Control-Allow-Method"] = "*"
    environ.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    return environ

@app.route("/login", methods=["POST"])
def login():
    logincred = request.get_data()
    logincred = json.loads(logincred)
    
    result = auth.checkpassword(logincred["id"], logincred["password"])

    return jsonify(result)



app.run(host='0.0.0.0', port=9000)

# if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=9000)
    # server = pywsgi.WSGIServer(('43.139.83.100', 9000), app)
    # server.serve_forever()