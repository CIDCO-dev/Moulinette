# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:10:14 2022

@author: Hydrograhe
"""


import numpy as np
import pickle
import sys
import pandas as pd
import os
from sys import platform

from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier


from sklearn.model_selection import train_test_split
from sklearn import metrics


def train_model(df):
    
    conditions = [
    (df['Nbrs_Moules'] == 0),
    (df['Nbrs_Moules'] > 0) & (df['Nbrs_Moules'] <= 3),
    (df['Nbrs_Moules'] > 3) & (df['Nbrs_Moules'] <= 9),
    (df['Nbrs_Moules'] > 9)
    ]

    values = ['Innexistant', 'Rare', 'Commun', 'Abondant']
    
    df['Mussels_Class'] = np.select(conditions, values)
    
    labels = df['GMM_Class']
    #labels = df['Nbrs_Moules']
    #labels =  df['Mussels_Class']
    #features = df[[f"H{i}"for i in range(1,17)]] ##Does not work uner linux
    features = df[["H{}".format(i) for i in range(1,17)]]
    
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
       
    pickle.dump(model,open("trained.model","wb"))
       
    report = metrics.classification_report(labelsTest, predictions,output_dict=False)
    
    accuracy_score = metrics.accuracy_score(labelsTest,predictions)
    
    #df_2 = pd.DataFrame(report).transpose()  ###if output_dict=True 
    
    
    sys.stderr.write("Totals: \n")
    sys.stderr.write("[*] {} accuracy: {}\n".format(modelName,accuracy_score))
    #print("[*] {} accuracy: {}\n".format(modelName,metrics.accuracy_score(labelsTest,predictions)))
    sys.stderr.write("{}".format(report))
    #print(report)
    sys.stderr.write("\n")
    sys.stderr.write("\n")


    return modelName,accuracy_score,report
 


################################################################################
# Main                                                                         #
################################################################################

if __name__ == "__main__":
    
    
        
    if len(sys.argv) != 3:
     	sys.stderr.write("Usage: train_model.py  training_data_or_folder_with_training_data   save_directory \n")
     	sys.exit(1)
    
    #sys.stderr.write("System : {}\n".format(platform))
    
    filename = sys.argv[1]
    save_directory = sys.argv[2]
    
    if os.path.exists(filename):
        
        if os.path.isfile(filename):
            file_list = [filename]
        else :
            file_list = os.listdir(filename)
            #file_list = [os.path.abspath(filename + file) for file in file_list]
            file_list = [filename + file for file in file_list]
       
    else :
        sys.stderr.write("The entry data does not exist\n") 
        
    #sys.stderr.write("{}\n".format(file_list))  
     
    for file in file_list :
        #sys.stderr.write("{}\n".format(os.path.abspath(file)))
        
        if platform == "linux2":
            file_name = file.split("/")[-1]
            file_name = file_name.split('.')[0]
            
        else:
            file_name = file.split("\\")[-1]
            file_name = file_name.split('.')[0]
            
        sys.stderr.write("Loading file : {} \n".format(file_name))
        
        
        df = pd.read_csv(file, delimiter = ',', header = 0, index_col = 0)
       

        modelName,accuracy_score,report = train_model(df)
        
        with open('{}Metrics_of_{}.txt'.format(save_directory,file_name), mode='w') as file_object:

            #print("[*] {} accuracy: {}\n".format(modelName,accuracy_score),"\n",report,"\n", file=file_object)  ##Does not work uner linux
            
            file_object.write("[*] {} accuracy: {}\n".format(modelName,accuracy_score) + "\n" + report + "\n")


    #filename = "C:\\Users\\Hydrograhe\\Documents\\GitHub\\Moulinette\\data\\dataset\\training_data_1m.csv"
    
