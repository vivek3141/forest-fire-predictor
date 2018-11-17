import numpy as np
import dill

data = "7,4,8,7,81.6,56.7,665.6,1.9,21.2,70,6.7,0"
data = np.array(list(map(float, data.split(",")))).reshape(-1,1).T
print(data.shape)
svm_model = dill.load(open("model.pkl", "rb"))
predicted = svm_model.predict(data)
print(predicted)
