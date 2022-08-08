import os
import sys
import csv
import numpy as np
import pickle
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

from sklearn import metrics

#import chardet
#import csvkit
####for pickle to work models should come frtom the same environment, not a mix of windows and linux

if len(sys.argv) != 2:
        sys.stderr.write("Usage: cat hackel | apply-model.py  model_file  \n")
        sys.exit(1)


modelFile = sys.argv[1]
#hackelFile = sys.argv[2]

model = pickle.load(open(modelFile,"rb"))

features = []
points = []


for input in sys.stdin:
	#print(input)
	#print(type(input))
	#print(input.split(','))
	row = input.split(',')
	#row =  [float(i)
	newRow= [] 
	for i in row:
		if len(i.split('.')) == 2:
			#print(i)
			newRow.append(float(i))
			#print(newRow[3:-2])
	if len(newRow) > 0:
		features.append(newRow[3:])
		points.append(newRow[:3])
	#print(features, points, type(features[0][0]))	features.append(newRow[3:-2])
	#points.append(newRow[:3])
	#print(features, points, type(features[0][0]))



"""
wtf = []

for i in range(len(features)-1):
	feature = features[i]
	if type(feature) == type(float()):
		wtf.append(feature)
"""

#print(features)

pos = 0

for row in features:
	try:
		classes = model.predict(np.array([row]))
	except:
		pos += 1
		continue;
	if len(classes) > 0:
		print(points[pos][0], points[pos][1], points[pos][2], classes[0])
	pos += 1
