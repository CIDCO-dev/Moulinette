# -*- coding: utf-8 -*-
"""
Created on Tue May 24 17:36:23 2022

@author: Hydrograhe
"""

import pandas as pd
import numpy as np

csv_file = "C:\\Users\Hydrograhe\Documents\GitHub\BenthicClassifier\data\listing_moules.csv"

df = pd.read_csv(csv_file, delimiter = ';', header = 0, usecols = [0,1,2,3,4,5],date_parser = ["Date"], dtype = {'Latitude': np.float32,'Longitude': np.float32, "Total": np.uint16})


repetition = df.duplicated(subset=['Latitude','Longitude'], keep=False)
indice_des_doublons = np.where(repetition == True)[0] 

ligne_a_suppr = np.array([])

for indice in indice_des_doublons: ##Supress duplicates keeping the most recent point
     lat,long = df.iloc[indice][['Latitude','Longitude']]
     doublons = df.loc[(df['Latitude'] == lat) & (df['Longitude'] == long)]
     date_max = doublons["Date"].max()
     indice = doublons.loc[doublons["Date"] != date_max].index.values
     ligne_a_suppr = np.append(ligne_a_suppr,indice)

###Some duplicates have the same coordinates AND the same date, we chose to the mean of the number of musels. 
repetition = df.duplicated(subset=['Latitude','Longitude'], keep=False)
indice_des_doublons = np.where(repetition == True)[0] 
for indice in indice_des_doublons:
     lat,long = df.iloc[indice][['Latitude','Longitude']]
     doublons = df.loc[(df['Latitude'] == lat) & (df['Longitude'] == long)]
     mean = int(doublons['Total'].mean())
     indice = doublons.index.values

     doublons.loc[doublons.index == indice[0]]['Total'] = mean
     ligne_a_suppr = np.append(ligne_a_suppr,indice[1:])
   
   
 
df = df.drop(ligne_a_suppr)
df = df.reset_index(drop = True)

repetition = df.duplicated(subset=['Latitude','Longitude'], keep=False)
indice_des_doublons = np.where(repetition == True)[0] 

if len(indice_des_doublons) == 0:
     
   file = open(".\\sorted_moules.txt","w")   
   df.to_csv(file, sep =',',header = True, index = True, line_terminator = '\n',float_format = '%.3f')		
   file.close()

else: 
   print("Des doublons sont encore presents")
