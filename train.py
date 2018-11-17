import pandas
import tensorflow as tf
from SVM import SVMTrainer

train = pandas.read_csv("training_data.csv")
print(train.head(517))
