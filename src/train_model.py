import csv
import numpy as np
import pickle
import sys
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV

"""
training data format:
x, y, z, hackel, gmm, groundTruth

"""


if len(sys.argv) != 2:
	sys.stderr.write("Usage: train_model.py FILE\n")
	sys.exit(1)

trainingFile = sys.argv[1]

#Load training data
with open(trainingFile) as f:
	reader = csv.reader(f, delimiter=" ")
	#next(reader)
	labeled_data = list(reader)
	sys.stderr.write("[+] Loaded {} training samples\n".format(len(labeled_data)))

	features = []
	labels = []
	coord = []
	
	for line in labeled_data:
		line = [ float(h) for h in line]
		features.append(line[3:-1])
		labels.append(int(line[-1]))
		coord.append(line[:3])


test_features = np.asarray(features[:200])
train_features = np.asarray(features[200:])
test_labels = np.asarray(labels[:200])
train_labels = np.asarray(labels[200:])


params = {
    "n_estimators": 500,
    "max_depth": 4,
    "min_samples_split": 5,
    "learning_rate": 0.01,
}

model = GradientBoostingRegressor(**params)
modelName = type(model).__name__ 
model.fit(train_features,train_labels)

sys.stderr.write("[+] Validating models...\n")

mse = mean_squared_error(test_labels, model.predict(test_features))
sys.stderr.write("The mean squared error (MSE) on test set: {:.4f}\n".format(mse))

#Save model
pickle.dump(model,open("trained_mussel_regression.model","wb"))

