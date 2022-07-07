# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 15:37:38 2022

@author: Hydrograhe
"""

import csv
import os
import numpy as np
import pickle
import sys
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
#from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing


from sklearn.model_selection import train_test_split
from math import sqrt

"""
training data format:
Id    X    Y    Z    id_moules    Nbrs_Moules    H1 H2 … H16    GMM_Class
"""

if len(sys.argv) != 3:
	sys.stderr.write("Usage: regression_model.py training_data_or_folder_with_training_data   model_save_directory\n")
	sys.exit(1)


trainingFile = sys.argv[1]
save_directory = sys.argv[2]

dic = {}
Flag = False
params = {
    "n_estimators": 500,
    "max_depth": 4,
    "min_samples_split": 5,
    "learning_rate": 0.01,  ##precise "loss": "squared_error" might provoke a bug, even though it's the default parameter.
}

if os.path.exists(trainingFile):
    
    if os.path.isfile(trainingFile):
        file_list = [trainingFile]
        flag = True
    else :
        file_list = os.listdir(trainingFile)
        #file_list = [os.path.abspath(filename + file) for file in file_list]
        file_list = [trainingFile + file for file in file_list]
   
else :
    sys.stderr.write("The entry data does not exist\n") 
 #Load training data
 
for file in file_list :
    #sys.stderr.write("{}\n".format(os.path.abspath(file)))
    
    if sys.platform == "linux2":
        file_name = file.split("/")[-1]
        file_name = file_name.split('.')[0]
        
    else:
        file_name = file.split("\\")[-1]
        file_name = file_name.split('.')[0]
        
    sys.stderr.write("Loading file : {} \n".format(file_name))
    
    #cols = [f'H{i}' for i in range(1,17)]
    cols = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16']
    df = pd.read_csv(file, delimiter = ',', header = 0, index_col = 0)
    features = df[cols].to_numpy()
    labels = df['GMM_Class']
    # test_features = df[cols].iloc[:200]
    # train_features = df[cols].iloc[200:]
    # test_labels = df["GMM_Class"].iloc[:200]
    # train_labels = df["GMM_Class"].iloc[200:]
    
    #Preprocess labels
    labelEncoder = preprocessing.LabelEncoder()
    labels_encoded = labelEncoder.fit_transform(labels)
 
    train_features, test_features, train_labels, test_labels = train_test_split(features,labels_encoded, test_size=0.2,random_state=109) #80/20 split
    #if len(train_features) > 0 and len(train_labels) > 0:

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
    
    if sys.platform == "linux2":
        file_name = file.split("/")[-1]
        
        
    else:
        file_name = file.split("\\")[-1]
    
    
    file_name = file_name.split(".")[0]
    
    
    dic[file_name] = sqrt(mse)
    
    #print(dir(model))
    if model.n_features_ != 16:
        sys.stderr.write("attention file: {} have {} features\n".format(file_name,model.n_features_))
        sys.stderr.write("attention file: {} doesn'thave 16 features\n")
    
    pickle.dump(model,open("{}regression_model_{}".format(save_directory,file_name),"wb"), protocol = 2)
    
        
  
# dic = {key: value for key, value in sorted(dic.items(), key=lambda item: item[1], reverse = False)}

# files_list =  list(dic.keys())[:5]
# RMSE_list =  list(dic.values())[:5]
    
# print("The minimal root mean squared error (RMSE) on test set are:\n")

# for i in range(5):
#       print("\t{} in file {} ".format(RMSE_list[i],files_list[i]))



if Flag:  ##Plot ssi un seul fichier en entree
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