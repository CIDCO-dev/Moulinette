# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 03:29:29 2022

@author: oscar
"""

import sys
import pandas as pd
import numpy as np
import scipy.spatial as sp



import generate_pre_training_data
import generate_training_data
import remove_overrepresented
import histo


################################################################################
# Main                                                                         #
################################################################################

if len(sys.argv) != 8:
	sys.stderr.write("Usage: automatize.py moules_nad.csv mbes_file_no_header.xyz Hackel_file.Hackel GMM_file radius(int or list) directory_to_save_data directory_to_save_histo\n")
	sys.exit(1)
	
labelfile= sys.argv[1]
mbes_file = sys.argv[2]
Hackel_file = sys.argv[3]
GMM_file = sys.argv[4]
radius = sys.argv[5]
data_dir = sys.argv[6]
histo_dir = sys.argv[7]


moules_dt = pd.read_csv(labelfile, delimiter = ';', header = 0, names = ['Y_moule','X_moule','nbrs_moules'], dtype = {'X_moule':np.float32,'Y_moule': np.float32,'nbrs_moules': np.uint16})
moules_dt = moules_dt.dropna()
moules_dt = moules_dt.reset_index(drop = True)

sys.stderr.write('Chargement du fichier mbes\n')
mbes_dt = pd.read_csv(mbes_file, delimiter = '\s+', header = 0, names = ['X','Y','Z'], dtype = {'X': np.float32,'Y': np.float64,'Z':np.float16})
sys.stderr.write("Fichier MBES chargé \n")
sys.stderr.write("{}\n".format(mbes_dt.info(verbose=False, memory_usage="deep")))

sys.stderr.write('Generation du kdTree\n')
kdtree = sp.KDTree(mbes_dt[['X','Y']])
sys.stderr.write('kdTree généré\n')
sys.stderr.write("Size of kdtree: {}\n".format(sys.getsizeof(kdtree)))


sys.stderr.write("Flag 1")
sys.stderr.write("radius: {}".format(radius))

dic = {}
if type(radius) == int:
    radius = [radius]
    sys.stderr.write("Flag 1.5")
if type(radius) == list:
    sys.stderr.write("Flag 2")
    for r in radius:
        sys.stderr.write("Flag 3")
        sys.stderr.write("Finding mbes points within {}m of a mussel point\n".format(r))
        df = generate_pre_training_data.nearest_neighbors(kdtree) ##gerer l exeption
        df = generate_pre_training_data.remove_duplicate(df) 
        
        dic["pre_training_data_r{}m".format(r)] = df

del (kdtree)

Hackel_dt = pd.read_csv(Hackel_file,delimiter = ',',header = None,
                        names = ['0','1','2','H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16'], 
                        usecols = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16'],
                        dtype = {'H1':np.float32,'H2':np.float32,'H3':np.float32,'H4':np.float32,'H5':np.float32,'H6':np.float32,'H7':np.float32,'H8':np.float32,'H9':np.float32,'H10':np.float32, 'H11':np.float32, 'H12':np.float32,'H13':np.float32,'H14':np.float32,'H15':np.float32,'H16':np.float32})
sys.stderr.write("Fichier hackel chargé \n")
sys.stderr.write("{}\n".format(Hackel_dt.info(verbose=False, memory_usage="deep")))

sys.stderr.write('Chargement du fichier GMM\n')
GMM_dt = pd.read_csv(GMM_file, delimiter = '\s+', header = None, names = ['X','Y','Z','GMM_Class'], usecols= ["GMM_Class"], dtype = np.uint8)
sys.stderr.write("Fichier GMM chargé \n")
sys.stderr.write("{}\n".format(GMM_dt.info(verbose=False, memory_usage="deep")))

dic_2 = {}
for key in dic:
    df = dic[key]
    r = key[-2] 
    df = generate_training_data.merge(df,Hackel_dt,GMM_dt)
    
    dic_2["training_data_r{}m".format(r)] = df
    
    dic_2["training_data_r{}m_weight".format(r)] = remove_overrepresented.weight_based_truncature(df)
    
    freq_list = [len(df.loc[df['Nbrs_moules'] == i]) for i in [4,7,10,12]]
    for freq in freq_list :
        dic_2["training_data_r{}m_freq{}".format(r,freq)] = remove_overrepresented.freq_max_based_truncature(df, freq)

del(dic)
del(Hackel_dt)
del(GMM_dt)
del(mbes_dt)

for key in dic_2:
    df = dic_2[key]
    sys.stderr.write('Saving the training data as {} in {}\n'.format(key,data_dir))
    file = open("{}{}.txt".format(data_dir,key),"w")   
    df.to_csv(file, sep =',',header = True, index = True, line_terminator = '\n')		
    file.close()
    sys.stderr.write('Generating histograms in {}\n'.format(histo_dir))
    histo.histo_3d(df,histo_dir,key)
    histo.histo_repartition_Moules(df,histo_dir,key)
    histo.histo_repartition_GMM(df,histo_dir,key) 