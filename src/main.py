from flask import Flask
from flask import request
import dill

app = Flask(__name__)


@app.route("/predict")
def predict():
    print("hi")
    X = request.args.get('x')
    print(X)
    svm_model = dill.load(open("model.pkl"))
    predicted = svm_model.predict(list(map(float, X.split(","))))
    print(predicted)
    return str(predicted)


@app.route("/")
def main():
    a = request.args.get('x')
    print(a)
    return a


app.run()
