import json
import datetime
from flask import *

import authenticator as auth
import dbapp as dbapp

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


@app.route("/getprof", methods=["POST"])
def getProfile():
    driverprof = request.get_data()
    driverprof = json.loads(driverprof)

    result = dbapp.getProfile(driverprof["id"])

    return result


@app.route("/getrace", methods=["POST"])
def getrace():
    today = datetime.datetime.today()
    today_str = today.strftime("%Y-%m-%d")

    result = dbapp.getRaceByStatus(status="ON REGIST")
    return result


@app.route("/getregist", methods=["POST"])
def getregist():
    gp = request.get_data()
    gp = json.loads(gp)

    result = dbapp.getRegist(gp["round"], gp["GP"])

    return result


@app.route("/driverregist", methods=["POST"])
def driverregist():
    driverreg = request.get_data()
    driverreg = json.loads(driverreg)

    result = dbapp.driverRegist(driverreg["id"], driverreg["gp"], driverreg["racegroup"])

    return result


@app.route("/driverwithdraw", methods=["POST"])
def driverwithdraw():
    driverwd = request.get_data()
    driverwd = json.loads(driverwd)

    result = dbapp.driverWithdraw(driverwd["id"], driverwd["gp"], driverwd["racegroup"])

    return result


@app.route("/getradiolist", methods=["POST"])
def getradiolist():
    return dbapp.getRadioList()


@app.route("/songorder", methods=["POST"])
def songorder():
    sorder = request.get_data()
    sorder = json.loads(sorder)

    result = dbapp.songorder(sorder["id"], sorder["songname"], sorder["artist"], sorder["album"], sorder["link"])

    return result    


app.run(host='0.0.0.0', port=9000)

# if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=9000)
    # server = pywsgi.WSGIServer(('43.139.83.100', 9000), app)
    # server.serve_forever()