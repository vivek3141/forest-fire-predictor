from flask import Flask
from flask import request
import dill
import numpy as np
import os
import datetime
import json
import urllib.request

app = Flask(__name__)


@app.route("/")
def main():
    return "<h1>Front Page</h1>"


@app.route("/predict")
def predict():
    c = list(map(int, request.args.get('c')[1:-1].split(",")))
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    x1 = -7.182288
    x2 = -6.515598
    y2 = 41.992531
    y1 = 41.732416
    X = int((9 * (c[0] - x1)) / (x2 - x1))
    Y = int((9 * (c[1] - y1)) / (y2 - y1))
    ffmc = 0.0
    dmc = 0.0
    dc = 0.0
    isi = 0.0
    temp = 0.0
    rh = 0.0
    wind = 0.0
    url = "api.openweathermap.org/data/2.5/weather?lat={}&lon={}".format(c[0], c[1])
    j = json.load(urllib.request.urlopen(url))
    data = str(X) + "," + str(Y) + "," + str(month) + "," + str(day) + "," + str(ffmc) + "," + \
           str(dmc) + "," + str(dc) + "," + str(isi) + "," + str(temp) + "," + str(rh) + "," + str(wind)
    data = np.array(list(map(float, data.split(",")))).reshape(-1, 1).T
    svm_model = dill.load(open("src/model.pkl", "rb"))
    predicted = svm_model.predict(data)
    return str(predicted[0])


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
