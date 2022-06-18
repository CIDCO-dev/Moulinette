# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 14:06:47 2022

@author: Hydrograhe
"""

import sys
import pandas as pd
import numpy as np
import scipy.spatial as sp


import histo

if len(sys.argv) != 3:
	sys.stderr.write("Usage: test.py directory_to_save_data directory_to_save_histo\n")
	sys.exit(1)
	
data_dir = sys.argv[1]
histo_dir = sys.argv[2]

file = "C:\\Users\Hydrograhe\Documents\\GitHub\\Moulinette\\data\\complete_training_data_1m_freq50.txt"
key = file.split('\\')[-1]

df = pd.read_csv(file, delimiter = '\s+', header = 0)

file = open(f"{data_dir}{key}.txt","w")   
df.to_csv(file, sep =',',header = True, index = True, line_terminator = '\n')		
file.close()

histo.histo_3d(df,histo_dir,key)
histo.histo_repartition_Moules(df,histo_dir,key)
histo.histo_repartition_GMM(df,histo_dir,key)

