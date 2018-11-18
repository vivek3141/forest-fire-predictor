import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import random
import dill
from sklearn import preprocessing, svm
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
data = "7,4,8,7,81.6,56.7,665.6,1.9,21.2,70,6.7,0"
data = np.array(list(map(float, data.split(",")))).reshape(-1,1).T