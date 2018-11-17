import pandas
import tensorflow as tf
from SVM import SVMTrainer

train = pandas.read_csv("data.csv")
model = SVMTrainer()
