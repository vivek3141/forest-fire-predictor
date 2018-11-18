from flask import Flask
from flask import request, make_response
import numpy as np
import os
import datetime
import json
import urllib.request
from src.fwi import *
from src.test import build_model
from keras import backend as K
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    resp = make_response("hello")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    """
    Y is Latitude, X is Longitude
    :return:
    """
    x1 = -7.182288
    x2 = -6.515598
    y2 = 41.992531
    y1 = 41.732416
    dates = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    c = list(map(float, request.args.get('c')[1:-1].split(",")))
    now = datetime.datetime.now()
    month = now.month
    day = dates.index(now.strftime("%A")) + 1
    if not (y1 <= c[0] <= y2):
        return "Outside Bounds"
    if not (x1 <= c[1] <= x2):
        return "Outside Bounds"
    x_p = (x2 - x1) / 9
    y_p = (y2 - y1) / 9
    delta_x = c[0] - y1
    delta_y = c[1] - x1
    X = int(delta_x/x_p)
    Y = int(delta_y/y_p)
    print(X, Y)
    url = "http://api.openweathermap.org/data/2.5/weather?lat={}&" \
          "lon={}&appid=997248ab2a9c56c05cf48c93efca9b27".format(c[0], c[1])

    j = json.load(urllib.request.urlopen(url))
    temp = 0
    wind = 0
    rh = 0
    rain = 0
    ffmc = 0
    dmc = 0
    dc = 0
    isi = 0
    try:
        temp = j['main']['temp'] - 273.15
    except KeyError:
        pass
    try:
        wind = j['wind']['speed'] * 3.6
    except KeyError:
        pass
    try:
        rh = j['main']['humidity']
    except KeyError:
        pass
    try:
        rain = ((j['rain']['3h']) / 6) / ((742300000 / 9) ** 2)
    except KeyError:
        pass
    try:
        ffmc = FFMC(temp, rh, wind, j['rain']['3h'] * 8, 57.45)
    except KeyError:
        pass
    try:
        dmc = DMC(temp, rh, j['rain']['3h'] * 8, 146.2, c[0], month)
    except KeyError:
        pass
    try:
        dc = DC(temp, j['rain']['3h'] * 8, 434.25, c[0], month)
    except KeyError:
        pass
    try:
        isi = ISI(wind, ffmc)
    except KeyError:
        pass

    data = str(X) + "," + str(Y) + "," + str(month) + "," + str(day) + "," + str(ffmc) + "," + str(
        dmc) + "," + str(dc) + "," + str(isi) + "," + str(temp) + "," + str(rh) + "," + str(wind) + ',' + str(
        rain)
    print(data)
    model = build_model()
    model.load_weights("./src/model_weights.h5")
    data = np.array(list(map(float, data.split(",")))).reshape(-1, 1).T
    predicted = model.predict(data)
    K.clear_session()
    return str(math.fabs(predicted[0][0]))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=False)
