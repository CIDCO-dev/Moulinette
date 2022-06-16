# -*- coding: utf-8 -*-
"""
Created on Mon May 16 14:21:06 2022

@author: Hydrograhe
"""

import pandas as pd
import numpy as np
import sys





def merge(df,hackel_dt,GMM_dt):
    



    sys.stderr.write("début merging \n")
    merged_dt = pd.merge(GMM_dt,df,left_index=True,right_on = 'id', how="inner")
    merged_dt = pd.merge(hackel_dt,merged_dt,left_index=True,right_on = 'id', how="inner")
    sys.stderr.write("fin merge \n")
    sys.stderr.write("debut reagensement \n")
    cols = ['id','X','Y','Z','id_moules','Nbrs_Moules', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16','GMM_Class']
    merged_dt = merged_dt[cols]
    sys.stderr.write("fin reagensement \n")
    sys.stderr.write("enregistrement result \n")

    # merged_dt = merged_dt.reset_index(drop = True)
    # merged_dt = merged_dt.astype({"id_mbes": np.uint32, "id_moules": np.uint16, "Nbrs_moules": np.uint8, 'X':np.float32, 'Y':np.float32, 'Z':np.float32, 
    #                         'H1':np.float32,'H2':np.float32,'H3':np.float32,'H4':np.float32,'H5':np.float32,'H6':np.float32,'H7':np.float32,'H8':np.float32,'H9':np.float32,
    #                         'H10':np.float32, 'H11':np.float32, 'H12':np.float32,'H13':np.float32,'H14':np.float32,'H15':np.float32,'H16':np.float32,'GMM_Class':np.uint8})

    # formats = {'X': '{:.3f}', 'Y': '{:.3f}', 'Z': '{:.3f}'}

    # for col, f in formats.items():
    #     merged_dt[col] = merged_dt[col].map(lambda x: f.format(x))
        
        
    return merged_dt
    
################################################################################
# Main                                                                         #
################################################################################
if __name__ == "__main__":
    if len(sys.argv) != 3:
     	sys.stderr.write("Usage:generate_training_data.py pre_training_data.txt hackel.Hackel  \n")
     	sys.exit(1)
     	
    #GMM_file = sys.argv[3]
    ppv = sys.argv[1]
    Hackel_file = sys.argv[2]
    
    df = pd.read_csv(ppv, delimiter = '\s+', header = 0, names = ['id_mbes','X','Y','Z','Nbrs_moules','id_moules'])
    
    sys.stderr.write("Chargement fichier de Hackel\n")
    hackel_dt = pd.read_csv(Hackel_file,delimiter = ',',header = None,names = ['0','1','2','H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16'], usecols = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16'])
    sys.stderr.write("Fichier hackel chargé \n")
    
    merged_dt = merge(df,hackel_dt)
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width',None):  # more options can be specified also
       print(merged_dt.to_string(index=False))
       
       

   