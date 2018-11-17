from flask import Flask
from flask import request
import dill
import numpy as np

app = Flask(__name__)


@app.route("/predict")
def predict():
    data = request.args.get('x')
    data = data[1:-1]
    data = np.array(list(map(float, data.split(",")))).reshape(-1, 1).T
    svm_model = dill.load(open("model.pkl", "rb"))
    predicted = svm_model.predict(data)
    return str(predicted[0])


app.run()
