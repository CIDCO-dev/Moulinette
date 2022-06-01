# -*- coding: utf-8 -*-
"""
Created on Mon May 16 14:21:06 2022

@author: Hydrograhe
"""

import pandas as pd
import numpy as np
import sys



if len(sys.argv) != 4:
 	sys.stderr.write("Usage: merge.py plus_proche_voisin.csv GMM.txt hackel.Hackel  \n")
 	sys.exit(1)
 	
GMM_file = sys.argv[2]
ppv = sys.argv[1]
Hackel_file = sys.argv[3]


GMM_dt = pd.read_csv(GMM_file, delimiter = '\s+', header = None, names = ['X','Y','Z','GMM_Classe'], usecols= ["GMM_Classe"])

ppv_dt = pd.read_csv(ppv, delimiter = ';', header = 0, names = ['id_mbes','X','Y','Z','Nbrs_moules','Classe','id_moules'])

sys.stderr.write("Chargement fichier de Hackel\n")
hackel_dt = pd.read_csv(Hackel_file,delimiter = ',',header = None,names = ['0','1','2','H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16'], usecols = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16'])
sys.stderr.write("Fichier hackel chargé \n")

sys.stderr.write("début merging \n")
merged_dt = pd.merge(GMM_dt,ppv_dt,left_index=True,right_on = 'id_mbes', how="inner")
merged_dt = pd.merge(hackel_dt,merged_dt,left_index=True,right_on = 'id_mbes', how="inner")
sys.stderr.write("fin merge \n")
sys.stderr.write("debut reagensement \n")
cols = ['id_mbes','X','Y','Z','id_moules','Nbrs_moules','Classe', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16','GMM_Classe']
merged_dt = merged_dt[cols]
sys.stderr.write("fin reagensement \n")
sys.stderr.write("enregistrement result \n")

merged_dt = merged_dt.reset_index(drop = True)
merged_dt = merged_dt.astype({"id_mbes": np.uint32, "id_moules": np.uint16, "Nbrs_moules": np.uint8, "GMM_Classe": np.uint8, 'X':np.float32, 'Y':np.float32, 'Z':np.float32, 
                        'H1':np.float32,'H2':np.float32,'H3':np.float32,'H4':np.float32,'H5':np.float32,'H6':np.float32,'H7':np.float32,'H8':np.float32,'H9':np.float32,
                        'H10':np.float32, 'H11':np.float32, 'H12':np.float32,'H13':np.float32,'H14':np.float32,'H15':np.float32,'H16':np.float32})

formats = {'X': '{:.3f}', 'Y': '{:.3f}', 'Z': '{:.3f}'}

for col, f in formats.items():
    merged_dt[col] = merged_dt[col].map(lambda x: f.format(x))
   
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width',None):  # more options can be specified also
   print(merged_dt)
   
   