import numpy as np
import dill

data = "2,2,3,7,89.3,51.3,102.2,9.6,11.5,39,5.8,0"
data = np.array(list(map(float, data.split(",")))).reshape(-1,1).T
print(data.shape)
svm_model = dill.load(open("model.pkl", "rb"))
predicted = svm_model.predict(data)
print(predicted)
