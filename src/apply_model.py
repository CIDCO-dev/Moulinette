# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 18:02:57 2022

@author: oscar
"""

import os
import sys
import csv
import pandas as pd
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


####for pickle to work ;odels should come frtom the same environment, not a mix of windows and linux

if len(sys.argv) != 4:
	sys.stderr.write("Usage: apply-model.py  model_file_or_model_directory  hackel-features_file  save_directory\n")
	sys.exit(1)


filename = sys.argv[1]
Hackel_file = sys.argv[2]
save_dir = sys.argv[3]


if os.path.exists(filename):

    if os.path.isfile(filename):
        file_list = [filename]

    else :
        file_list = os.listdir(filename)
        #file_list = [os.path.abspath(filename + file) for file in file_list]
        file_list = [filename + file for file in file_list]
   
else :
    sys.stderr.write("The entry data does not exist\n") 
    

sys.stderr.write("[+] Loading hackel features")

#sys.stderr.write("{}\n".format(modelFilename))

df = pd.read_csv(Hackel_file,delimiter = ',',header = None,nrows = None,
                        names = ['X','Y','Z','H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16'], 
                        dtype = {'H1':np.float32,'H2':np.float32,'H3':np.float32,'H4':np.float32,'H5':np.float32,'H6':np.float32,'H7':np.float32,'H8':np.float32,'H9':np.float32,'H10':np.float32, 'H11':np.float32, 'H12':np.float32,'H13':np.float32,'H14':np.float32,'H15':np.float32,'H16':np.float32})


sys.stderr.write("[+] Loaded {} hackel features".format(len(df)))

features = df[['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16']].to_numpy()

for file in file_list :
    model = pickle.load(open(file,"rb"))

    #Load training data
    if model:
        if sys.platform == "linux2":
            file_name = file.split("/")[-1]
            file_name = file_name.split('.')[0]
            
        else:
            file_name = file.split("\\")[-1]
            file_name = file_name.split('.')[0]
            
        sys.stderr.write("Applying model: {} \n".format(file_name))
        
        classes = model.predict(features);
    
    
        df_2 = df[['X','Y','Z']]
        # df_2['Classes'] = classes
        df_2.insert(len(df_2.columns),"Classes",classes)
        

        
        file = open("{}{}.csv".format(save_dir,file_name),"w")   
        #sys.stderr.write("saving file: {} \n".format(file))
        df_2.to_csv(file, sep =',',header = True, index = False, line_terminator = '\n')
    
    
    else:
    	sys.stderr.write("Couldn't load model\n")