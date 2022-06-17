# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:06:50 2022

@author: Hydrograhe
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import matplotlib.cm as cm 
from matplotlib import colors
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist

import pandas as pd
from pandas.plotting import table
import numpy as np
import sys
import os




def histo_3d(df,histo_dir,file_name):
    x = df['GMM_Class'].values
    y = df["Nbrs_Moules"].values
    classes = np.unique(y)
    H, xedges, yedges = np.histogram2d(x, y, bins= [5,len(classes)], range=[[0, 5], [0, max(classes)]])
     
    fig = plt.figure()
    #ax = fig.add_subplot(121,projection='3d')
    ax = fig.add_subplot(projection='3d')
    
    
    # Construct arrays for the anchor positions of the 16 bars.
    xpos, ypos = np.meshgrid(xedges[:-1] - 0.25, yedges[:-1] -0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0
    
    # Construct arrays with the dimensions for the 16 bars.
    dx = dy = 0.5 * np.ones_like(zpos)
    dz = H.ravel()
    
    cmap = cm.get_cmap('RdYlBu_r')   # Get desired colormap
    
    log_rgba = cmap(np.log(dz)/np.log(np.max(dz)))
        
    rgba = cmap(dz/np.max(dz))
    
    #rgba = [colors.to_rgba('blue')] * 3 + [colors.to_rgba('green')] * 3 + [colors.to_rgba('yellow')] * 3 + [colors.to_rgba('orange')] * 3 + [colors.to_rgba('red')] * 3 
    
    
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz,color = rgba, alpha = 0.9)
    # ax.set_yticks([0.5, 1.5,2.5,3.5])
    # ax.set_yticklabels(['Inexistant (0 moules)', 'Rare (<= 3 moules)', 'Commun (<= 10 moules)','Abondant (>10 moules)'], horizontalalignment = 'left')
    
    # columns = np.arange(100)
    # rows = [f'Classe {i}' for i in range(5)]
    
    # the_table = plt.table(cellText=H,
    #                    rowLabels=rows,
    #                    colLabels=columns,
    #                    loc='bottom')
    
    ax.set_zlabel('Nombres de points mbes', labelpad = 6)
    ax.set_ylabel("Nombres de moules", labelpad = 6)
    ax.set_xlabel("GMM Classe", labelpad = 6)
    
    ax.set_title('Corrélation GMM/Habitats de moules', loc = 'right')
    
    #ax = fig.add_subplot(122)
    # ax = plt.figure()
    #df = pd.DataFrame(data=H, columns =classes)
    # table(ax, df, loc='bottom')
      

    plt.savefig('{}histo_3d_{}.png'.format(histo_dir,file_name),format = 'png',dpi = 300,bbox_inches='tight')
    plt.close()


def flat_histo_3d(df,histo_dir,file_name):
   x = df['GMM_Class'].values
   y = df["Nbrs_Moules"].values
   classes = np.unique(y)
   H, xedges, yedges = np.histogram2d(x, y, bins= [5,len(classes)], range=[[0, 5], [0, max(classes)]])

   fig = plt.figure()
   ax = fig.add_subplot(projection='3d')
   
   #colors = ['r', 'g', 'b']
   cmap = cm.get_cmap('jet')   # Get desired colormap
   rgba = cmap(np.log(H.T)/np.log(np.max(H.T)))
   
   x = [0,1,2,3,4]
   i = 0
   H = H.T
   max_z = np.max(H)
   
   for hauteur in H:
      
   
       #print(hauteur)
   
       log_rgba = cmap(np.log(hauteur)/np.log(max_z))
       rgba = cmap(hauteur/max_z)
       #print(rgba)
       #cs = [colors[i]] * len(x)
   
       # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
       ax.bar(x,hauteur,zs=i,zdir='y',color = rgba, alpha=0.9)
       i = i + 1
   
   ax.set_xlabel('X')
   ax.set_ylabel('Y')
   ax.set_zlabel('Z')
   
   # On the y axis let's only label the discrete values that we have data for.
   # ax.set_yticks([0.5, 1.5,2.5,3.5])
   # ax.set_yticklabels(['Inexistant (0 moules)', 'Rare (<= 3 moules)', 'Commun (<= 10 moules)','Abondant (>10 moules)'], horizontalalignment = 'left')
   
   ax.set_zlabel('Nombres de points mbes', labelpad = 6)
   ax.set_ylabel("Nombres de moules", labelpad = 6)
   ax.set_xlabel("GMM Classe ", labelpad = 6)
   ax.set_ylabel("")
   
   ax.set_title('Corrélation GMM/Habitats de moules', loc = 'center')
   #plt.set_zscale('log')
   
   plt.savefig('{}flat_histo_3d_{}.png'.format(histo_dir,file_name),format = 'png', dpi = 300,bbox_inches='tight') #quality = 95 )
   plt.close()
   
def histo_repartition_GMM(df,histo_dir,file_name):
    x = df['GMM_Class'].values
    
    plt.figure()
    
    n, bins, patches = plt.hist(x, bins = [0,1,2,3,4,5], rwidth = 0.5, color = 'g', edgecolor = 'black')  
    plt.xticks([0.5,1.5,2.5,3.5,4.5],labels = ['0','1','2','3','4'])
    #plt.xlim(0.25, max(x) + 1)
    plt.xlabel("Classe GMM")
    plt.ylabel("Nbrs de points mbes")
    plt.title("Histogramme de répartition des classes GMM")
    
    
    cmap = cm.get_cmap('RdYlBu_r')   # Get desired colormap
    color_ratio = np.log(n)/np.log(np.max(n))
    for c, p in zip(color_ratio, patches):
        plt.setp(p, 'facecolor', cmap(c))
    

    
    plt.savefig("{}GMM_repartition_{}.png".format(histo_dir,file_name),format = 'png', dpi = 300) 
    plt.close()
def histo_repartition_Moules(df,histo_dir,file_name):
    max_dist = find_max_dist_cloud(df)
    
    plt.figure()
    
    z = df['Nbrs_Moules'].values
    
    n, bins, patches = plt.hist(z,np.arange(max(z)+1), color = 'g', edgecolor = 'black')  
    
    plt.xticks(np.arange(110, step = 10))
    #plt.xlim(0, max(z) + 1)
    plt.xlabel("Nombres de moules")
    plt.ylabel( "Nbrs de points mbes à {}m ou moins".format(max_dist))
    plt.title("Histogramme de répartition des moules")
    
    
    cmap = cm.get_cmap('RdYlBu_r')   # Get desired colormap
    color_ratio = np.log(n)/np.log(np.max(n))
    for c, p in zip(color_ratio, patches):
        plt.setp(p, 'facecolor', cmap(c))
    

    
    plt.savefig("{}Moules_repartition_{}.png".format(histo_dir,file_name),format = 'png', dpi = 300) 
    plt.close()
def find_max_dist_cloud(df):
    length = np.bincount(df['id_moules'])   
    id_moule = np.argmax(length)
    df = df.loc[df['id_moules'] == id_moule]
    if len(df) >= 3:
        points = df[['X','Y']].values
        hull = ConvexHull(points)
        
        # Extract the points forming the hull
        hullpoints = points[hull.vertices,:]
        
        # Naive way of finding the best pair in O(H^2) time if H is number of points on
        # hull
        hdist = cdist(hullpoints, hullpoints, metric='euclidean')
        
    else :
        hdist = 0
    return int((np.max(hdist)+1)/2)


            
            
################################################################################
# Main                                                                         #
################################################################################

if __name__ == "__main__":

    if len(sys.argv) != 3:
     	sys.stderr.write("Usage: histo.py   training_data_or_folder_with_training_data   save_directory \n")
     	sys.exit(1)
     	
    
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

    sys.stderr.write("{}\n".format(file_list))

    
    for file in file_list :
        #sys.stderr.write("{}\n".format(os.path.abspath(file)))
        
        file_name = file.split('\\')[-1]
        file_name = file_name.split('.')[0]
        
        sys.stderr.write("Loading file : {} \n".format(file_name))
        
        
        df = pd.read_csv(file, delimiter = ',', header = 0, index_col = 0)
    
        max_dist = find_max_dist_cloud(df)

    
        sys.stderr.write("Plotting histograms \n")
        
        #flat_histo_3d(df,histo_dir,file_name)  
        histo_3d(df,save_directory,file_name)
        histo_repartition_GMM(df,save_directory,file_name)
        histo_repartition_Moules(df,save_directory,file_name)
        

