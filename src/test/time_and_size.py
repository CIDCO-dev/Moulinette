# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 13:24:58 2022

@author: Hydrograhe
"""
import pandas as pd
import numpy as np
import scipy.spatial as sp
import sys
import sklearn.neighbors  as sk
import time

mussels_file = "C:\\Users\Hydrograhe\Documents\\GitHub\\Moulinette\\data\\mussels\\moules_nad.csv"
mbes_file = "C:\\Users\Hydrograhe\Documents\\GitHub\\Moulinette\\data\\MBES\\Combine_secteur_Quebec_no_header.xyz"
Hackel_file = "C:\\Users\Hydrograhe\Documents\\GitHub\\Moulinette\\data\\"
GMM_file = "C:\\Users\Hydrograhe\Documents\\GitHub\\Moulinette\\data\\GMM\\Nad83_gmm-class.xyzC"


moules_dt = pd.read_csv(mussels_file, delimiter = ';', header = 0, names = ['Y_moule','X_moule','nbrs_moules'], dtype = {'X_moule':np.float32,'Y_moule': np.float32,'nbrs_moules': np.uint16},nrows = 100)
moules_dt = moules_dt.dropna()
moules_dt = moules_dt.reset_index(drop = True)

mbes_dt = pd.read_csv(mbes_file, delimiter = '\s+', header = 0, names = ['X','Y','Z'], nrows = 1000000, dtype = {'X': np.float32,'Y': np.float64,'Z':np.float16},float_precision = 'round_trip')
# formats = {'X': '{:.3f}', 'Y': '{:.3f}', 'Z': '{:.3f}'}
# for col, f in formats.items():
#     mbes_dt[col] = mbes_dt[col].map(lambda x: f.format(x))
    

#Hackel_dt = pd.read_csv(Hackel_file,delimiter = ',',header = None,names = ['0','1','2','H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16'], usecols = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','H14','H15','H16'])
  

# GMM_dt = pd.read_csv(GMM_file, delimiter = '\s+', header = None, names = ['X','Y','Z','GMM_Class'], usecols= ["GMM_Class"],nrows = 100, dtype = np.uint8)  

radius = 10000

start_time = time.time()
kdtree = sp.KDTree(mbes_dt[['X','Y']])
print("--- scipy tree {}s seconds --- \n".format((time.time() - start_time)))
print("--- scipy tree size {} --- \n".format(sys.getsizeof(kdtree)))

start_time = time.time()
ball_tree = sk.BallTree(mbes_dt[['X','Y']])
print("--- sklearn Balltree %s seconds ---\n" % (time.time() - start_time))
print("--- sklearn Balltree size {} --- \n".format(sys.getsizeof(ball_tree)))

start_time = time.time()
sktree = sk.KDTree(mbes_dt[['X','Y']])
print("--- sklearn KDtree %s seconds ---\n" % (time.time() - start_time))
print("--- sklearn KDtree size {} --- \n".format(sys.getsizeof(sktree)))


points = kdtree.query_ball_point(moules_dt[['X_moule','Y_moule']], r = radius)

points_bis = ball_tree.query_radius(moules_dt[['X_moule','Y_moule']], radius)






#print(moules_dt.iloc[:5])
#print('moules_dt :\n',moules_dt.memory_usage(deep=True))
#print(moules_dt['Y_moule'][0])


# print(mbes_dt.iloc[:5])
# print('mbes_dt :\n',mbes_dt.memory_usage(deep=True))
#print(mbes_dt['Y'][0])

# print(GMM_dt.iloc[:5])
#print('moules_dt :\n',GMM_dt.memory_usage(deep=True))


