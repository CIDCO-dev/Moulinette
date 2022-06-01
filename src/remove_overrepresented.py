# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 14:04:32 2022

@author: Hydrograhe
"""
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
from matplotlib import colors



################################################################################
# Main                                                                         #
################################################################################


if len(sys.argv) != 3:
	sys.stderr.write("Usage: remove_overrepresented.py training_data.txt maximum_frequency_allowed \n")
	sys.exit(1)
	

filename = sys.argv[1]
freq_max = int(sys.argv[2])

#filename = "C:\\Users\Hydrograhe\Documents\\GitHub\\Moulinette\\data\\trained_data.csv"


#freq_max = 75
ligne_a_suppr = []
df = pd.read_csv(filename, delimiter = '\s+', header = 0)

nbrs_moules = df['Nbrs_moules']
frequency = np.bincount(nbrs_moules)


for i in range(len(frequency)):
    ratio = frequency[i]/freq_max
    if ratio > 1:
        df_1 = df.loc[df['Nbrs_moules'] == i]
        #print(i)
        id_moules = df_1['id_moules'].drop_duplicates().values
        #print(id_moules)
        for id_ in id_moules:
            df_2 = df_1.loc[df_1['id_moules'] == id_]
            n = len(df_2)
            if n < ratio:
                ligne_a_suppr = np.append(ligne_a_suppr, df_2.index.values[1:])
            else:
                keeping = int(n//ratio)
                ligne_a_suppr = np.append(ligne_a_suppr, df_2.index.values[keeping:])
                
                
df = df.drop(ligne_a_suppr)
df = df.reset_index(drop = True)
                
# nbrs_moules = df['Nbrs_moules']
# frequency = np.bincount(nbrs_moules)       

with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width',None):  # more options can be specified also
   print(df.to_string(index=False))


