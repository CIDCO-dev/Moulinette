# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:10:14 2022

@author: Hydrograhe
"""

import csv
import numpy as np
import pickle
import sys
import pandas as pd

from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier


from sklearn.model_selection import train_test_split
from sklearn import metrics

# if len(sys.argv) != 2:
# 	sys.stderr.write("Usage: train.py complete-training-data.txt\n")
# 	sys.exit(1)

#trainingFile = sys.argv[1]

trainingFile = "C:\\Users\Hydrograhe\Documents\GitHub\Moulinette\data\complete_training_data_1m_freq50.txt"

df = pd.read_csv(trainingFile, delimiter = '\s+', header = 0)
labels = df['GMM_Class']
features = df[[f"H{i}"for i in range(1,17)]]

#Preprocess labels
labelEncoder = preprocessing.LabelEncoder()
labels_encoded = labelEncoder.fit_transform(labels)
   
labelDictionary = dict(zip(labelEncoder.transform(labelEncoder.classes_),labelEncoder.classes_))
   
print(labelDictionary)
   
featuresTrain, featuresTest, labelsTrain, labelsTest = train_test_split(features,labels_encoded, test_size=0.2,random_state=109) #80/20 split
   
sys.stderr.write("[+] Training model...\n")
   
model = GradientBoostingClassifier()
   
modelName = type(model).__name__ 
   
model.fit(featuresTrain,labelsTrain)
   
sys.stderr.write("[+] Validating models...\n")
   
predictions = model.predict(featuresTest)
   
#predictions = np.asarray([np.argmax(line) for line in predictions])

#Save model
pickle.dump(model,open("trained.model","wb"))
   
   
sys.stderr.write("Totals: \n")
sys.stderr.write("[*] {} accuracy: {}\n".format(modelName,metrics.accuracy_score(labelsTest,predictions)))
sys.stderr.write(metrics.classification_report(labelsTest, predictions))
sys.stderr.write("\n")
sys.stderr.write("\n")