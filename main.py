from flask import Flask
from flask import request, make_response
import pickle
import numpy as np
import os
import datetime
import json
import urllib.request
from src.fwi import *
from src.test import build_model

app = Flask(__name__)


@app.route("/")
def home():
    resp = make_response("hello")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    c = list(map(float, request.args.get('c')[1:-1].split(",")))
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    x1 = -7.182288
    x2 = -6.515598
    y2 = 41.992531
    y1 = 41.732416
    X = int((9 * (c[0] - x1)) / (x2 - x1))
    Y = int((9 * (c[1] - y1)) / (y2 - y1))
    url = "http://api.openweathermap.org/data/2.5/weather?lat={}&" \
          "lon={}&appid=997248ab2a9c56c05cf48c93efca9b27".format(c[0], c[1])

    j = json.load(urllib.request.urlopen(url))
    print(j)
    try:
        temp = j['main']['temp'] - 273.15
        wind = j['wind']['speed'] * 3.6
        rh = j['main']['humidity']
        rain = ((j['rain']['3h']) / 6) / ((742300000 / 9) ** 2)
        ffmc = FFMC(temp, rh, wind, j['rain']['3h'] * 8, 57.45)
        dmc = DMC(temp, rh, j['rain']['3h'] * 8, 146.2, c[0], month)
        dc = DC(temp, j['rain']['3h'] * 8, 434.25, c[0], month)
        isi = ISI(wind, ffmc)
    except:
        return "Data Not Found!"
    data = str(X) + "," + str(Y) + "," + str(month) + "," + str(day) + "," + str(ffmc) + "," + str(
        dmc) + "," + str(dc) + "," + str(isi) + "," + str(temp) + "," + str(rh) + "," + str(wind) + ',' + str(
        rain)
    model = build_model()
    model.load_weights("./src/model_weights.h5")
    data = np.array(list(map(float, data.split(",")))).reshape(-1, 1).T
    predicted = model.predict(data)
    return str(predicted[0][0])


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
