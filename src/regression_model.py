import csv
import numpy as np
import pickle
import sys
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
#from sklearn import metrics
from sklearn.metrics import mean_squared_error

"""
training data format:
x, y, z, nb_moule, 16 hackel features, gmm class

"""

if len(sys.argv) != 2:
	sys.stderr.write("Usage: train.py training-data.txt\n")
	sys.exit(1)

trainingFile = sys.argv[1]

#Load training data
with open(trainingFile) as f:
	reader = csv.reader(f)
	next(reader)
	labeled_data = list(reader)
	sys.stderr.write("[+] Loaded {} training samples\n".format(len(labeled_data)))

	features = []
	labels = []
	
	for line in labeled_data:
		line = [ float(h) for h in line]
		features.append(line[5:])
		labels.append(int(line[4]))


test_features = np.asarray(features[:200])
train_features = np.asarray(features[200:])
test_labels = np.asarray(labels[:200])
train_labels = np.asarray(labels[200:])


params = {
    "n_estimators": 500,
    "max_depth": 4,
    "min_samples_split": 5,
    "learning_rate": 0.01,
    "loss": "squared_error",
}

model = GradientBoostingRegressor(**params)

modelName = type(model).__name__ 

model.fit(train_features,train_labels)




sys.stderr.write("[+] Validating models...\n")

#predictions = model.predict(test_features)

"""
for i in range(len(predictions)):
	print(predictions[i], " : ", test_labels[i] )
"""
mse = mean_squared_error(test_labels, model.predict(test_features))
print("The mean squared error (MSE) on test set: {:.4f}".format(mse))



feature_importance = model.feature_importances_
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + 0.5
fig = plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.barh(pos, feature_importance[sorted_idx], align="center")
#plt.yticks(pos, np.array(diabetes.feature_names)[sorted_idx])
plt.title("Feature Importance (MDI)")

"""
result = permutation_importance(
    reg, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2
)
sorted_idx = result.importances_mean.argsort()
plt.subplot(1, 2, 2)
plt.boxplot(
    result.importances[sorted_idx].T,
    vert=False,
    labels=np.array(diabetes.feature_names)[sorted_idx],
)
plt.title("Permutation Importance (test set)")
fig.tight_layout()
"""
plt.show()
