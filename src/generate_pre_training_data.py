# -*- coding: utf-8 -*-
"""
Created on Tue May 10 14:21:10 2022

@author: Oscar
"""
import sys
import pandas as pd
import numpy as np
import scipy.spatial as sp



def nearest_neighbors(kdtree,moules_dt,mbes_dt,radius, mbes_file):

		
   points = kdtree.query_ball_point(moules_dt[['X_moule','Y_moule']], r = radius)
   
   moules = points.nonzero()[0]  ##donne l'ensemble des moules qui ont des points a proximite
   
   if len(moules) == 0:
       sys.exit("No point in the {} file is within {}m of a mussel.\n".format(mbes_file,radius))
   
		
   dic = dict()
		
   for k in moules: 
			
       df = mbes_dt.iloc[points[k]]  ##ensemble des points a proximite de la k_eme moule
			
       #df3["Classe"] = moules_dt.Classe[k]   ## ajoute une colonne contenant la classe de la k_eme moule
                                              ## retourne une erreur
       
       df.insert(len(df.columns),"Nbrs_Moules",moules_dt.nbrs_moules[k])
       #df.insert(len(df.columns),"Classe",moules_dt.Classe[k])  ##ne retourne pas d'erreur
       
       
       dic[str(k)] = df
			
      
   df = pd.concat(dic)
		
   df = df.rename_axis(index=["moules", "id"])	 
		
   return df

def remove_duplicate(df,moules_dt):
      
     
     sys.stderr.write('Start data sorting\n')
     repetition = df.index.droplevel(0).duplicated(keep = False) 
     indice_des_doublons = np.where(repetition == True)[0]  ##donnent les indices des lignes de df pour lesquelles l'indice n est pas unique. i-e: ces points sont voisins de plusieurs moules

     ligne_a_suppr_3 = []
     iteration = 0
     k = 1
     n =len(indice_des_doublons)

     for indice in indice_des_doublons:
          iteration = iteration + 1
          points = df.iloc[indice].name[1]  ##id du point voisin de plusieurs moules
          doublons = df.xs(points,level = 1) ##dataframe contenant les lignes doublons
          dist = []
          
          for moules in doublons.index:  ##Determination des distances entre le point et chaque moule voisine 
             coord_points = doublons.loc[moules][['X','Y']].values
             coord_moules = moules_dt[['X_moule','Y_moule']].iloc[int(moules)].values
             dist.append(np.linalg.norm(coord_points - coord_moules))
          
             
          indice_dist_min = np.argmin(dist)  ##donne la moule la plus proche du point            			
          doublons = doublons.drop(doublons.index[indice_dist_min])
          ligne_a_suppr = tuple(zip(doublons.index.values,np.ones(len(doublons),dtype = int)*points))##on supprime dans df les doublons, on ne garde que la ligne correspondant a la moule la plus proche
          
          for couple in ligne_a_suppr:
             ligne_a_suppr_3.append(couple)
            
          if iteration == n//10*k : ##bare de chargement
             sys.stderr.write('Data sorting: {}% \n'.format(k * 10))
             k = k + 1
             
     df = df.drop(ligne_a_suppr_3)
     df = df.reset_index()
     df['id_moules'] = df.pop('moules')

     return df
   

################################################################################
# Main                                                                         #
################################################################################
if __name__ == "__main__":
    
    if len(sys.argv) != 4:
     	sys.stderr.write("Usage: plus_proche_voisin_linux.py moules_nad.csv mbes_file_no_header.xyz radius \n")
     	sys.exit(1)
    	
    radius = int(sys.argv[3])
    labelfile= sys.argv[1]
    mbes_file = sys.argv[2]
    
    
    
    sys.stderr.write("Loading ground truthing from {} using a radius of {}m \n".format(labelfile,radius))
    
    
    moules_dt = pd.read_csv(labelfile, delimiter = ',', header = 0, names = ['Y_moule','X_moule','nbrs_moules'])
    moules_dt = moules_dt.dropna()
    moules_dt = moules_dt.reset_index(drop = True)
    
    
                  
    sys.stderr.write('Loading MBES file {}\n'.format(mbes_file))
    
    mbes_dt = pd.read_csv(mbes_file, delimiter = '\s+', header = 0, names = ['X','Y','Z'])
    
       		
    sys.stderr.write('Generating  kdTree\n')
    
    kdtree = sp.KDTree(mbes_dt[['X','Y']])
    
    sys.stderr.write("Search for points mbes a {}m or less of a mussel\n".format(radius))
    
    
    df = nearest_neighbors(kdtree,moules_dt,mbes_dt,radius, mbes_file)
    
    
    df = remove_duplicate(df,moules_dt)
    
    #sys.stderr.write("Enregistrement du fichier: .\\classification_{}.txt\n".format(hackelFile[:-7]))
    # file = open(".\\classification_{}.txt".format(hackelFile[:-7]),"w")   
    # df.to_csv(file, sep ='\t',header = True, index = True, line_terminator = '\n',float_format = '%.3f')		
    # file.close()
    sys.stderr.write("Saving file \n")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None,'display.width',None):  # more options can be specified also
        print(df.to_string(index=False))
    
       
            
