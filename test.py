import pandas
from SVM import SVMTrainer
from kernel import Kernel
import dill as d
import numpy as np

train = pandas.read_csv("data.csv")
trainer = SVMTrainer(kernel=Kernel.gaussian(1), c=0.1)
X = np.array(train[['X', 'Y', 'month', 'day', 'FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain']])
y = np.array(train['area'])
model = trainer.train(X, y)
d.dump(model, open("model.pkl", "wb"))
print(X[-3], y[-3])
print(model.predict(X[-3]))

