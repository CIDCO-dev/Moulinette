# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:06:50 2022

@author: Hydrograhe
"""


import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
from matplotlib import colors

result_file = 'C:\\Users\\Hydrograhe\\Documents\\GitHub\\Moulinette\\data\\trained_data.csv'

result = pd.read_csv(result_file, delimiter = ';', header = 0)
result = result.dropna()
 
# dic = {}
   
# for txt in pd.unique(result['Classe']):
#     test1 = result.loc[result['Classe'] == txt]
#     dic['classe de moules {}'.format(txt)] = len(test1)
#     for i in range (int(max(result['GMM_Classe']))):

#       test2 = test1.loc[result['GMM_Classe'] == i]
#       #print(txt,': nbrs de moules ds la classe',i,':',len(test2))
#       dic['nombre de points de classe {} parmis les zones de moules {}:'.format(i,txt)] =len(test2)
      

x = result['GMM_Classe'].values
y= []
for classe in result['New_Classe'] :
   if classe == 'Inexistant' :
      y.append(0)
   elif classe == 'Rare':
      y.append(1)
   elif classe == 'Commun':
      y.append(2)
   else :
      y.append(3)


H, xedges, yedges = np.histogram2d(x, y, bins= [5,4], range=[[0, 5], [0, 4]])

def histo_3d(x,y,H,xedges,yedges):

   fig = plt.figure()
   ax = fig.add_subplot(projection='3d')
   
   
   # Construct arrays for the anchor positions of the 16 bars.
   xpos, ypos = np.meshgrid(xedges[:-1] - 0.25, yedges[:-1] -0.25, indexing="ij")
   xpos = xpos.ravel()
   ypos = ypos.ravel()
   zpos = 0
   
   # Construct arrays with the dimensions for the 16 bars.
   dx = dy = 0.5 * np.ones_like(zpos)
   dz = H.ravel()
   
   cmap = cm.get_cmap('jet')   # Get desired colormap

   #rgba = [cmap((k-min_height)/max_height) for k in dz] 
   
   rgba = cmap(np.log(dz)/np.log(np.max(dz)))
   
   #rgba = [colors.to_rgba('blue')] * 3 + [colors.to_rgba('green')] * 3 + [colors.to_rgba('yellow')] * 3 + [colors.to_rgba('orange')] * 3 + [colors.to_rgba('red')] * 3 
   
   
   ax.bar3d(xpos, ypos, zpos, dx, dy, dz,color = rgba,norm=colors.LogNorm(), zsort='average')
   ax.set_yticks([0.5, 1.5,2.5,3.5])
   ax.set_yticklabels(['Inexistant (0 moules)', 'Rare (<= 3 moules)', 'Commun (<= 10 moules)','Abondant (>10 moules)'], horizontalalignment = 'left')
   
   
   ax.set_zlabel('Nombres de points', labelpad = 6)
   #ax.set_ylabel("Classe de moules", labelpad = 15)
   ax.set_xlabel("GMM Classe", labelpad = 6)
   
   ax.set_title('Corrélation GMM/Habitats de moules', loc = 'right')
   
   plt.savefig('histo_3d.png',format = 'png',dpi = 300,bbox_inches='tight')
   


def flat_histo_3d(x,y,H):

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
   
       rgba = cmap(np.log(hauteur)/np.log(max_z))
       #print(rgba)
       #cs = [colors[i]] * len(x)
   
       # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
       ax.bar(x,hauteur,zs=i,zdir='y',color = rgba, alpha=0.9)
       i = i + 1
   
   ax.set_xlabel('X')
   ax.set_ylabel('Y')
   ax.set_zlabel('Z')
   
   # On the y axis let's only label the discrete values that we have data for.
   ax.set_yticks([0.5, 1.5,2.5,3.5])
   ax.set_yticklabels(['Inexistant (0 moules)', 'Rare (<= 3 moules)', 'Commun (<= 10 moules)','Abondant (>10 moules)'], horizontalalignment = 'left')
   
   ax.set_zlabel('Nombres de moules', labelpad = 6)
   #ax.set_ylabel("Classe de moules", labelpad = 15)
   ax.set_xlabel("GMM Classe ", labelpad = 6)
   
   ax.set_title('Corrélation GMM/Habitats de moules', loc = 'center')
   #plt.set_zscale('log')
   
   plt.savefig('flat_histo_3d.png',format = 'png', dpi = 300,bbox_inches='tight') #quality = 95 )
   
   
def histo_2d(x,y):
    

    n, bins, patches = plt.hist(x, bins = [0,1,2,3,4,5], rwidth = 0.5, color = 'g', edgecolor = 'black')  
    plt.xticks([0.5,1.5,2.5,3.5,4.5],labels = ['0','1','2','3','4'])
    plt.xlabel("Classe GMM")
    plt.ylabel("Nbrs de points mbes")
    plt.title("Histogramme de répartition des classes GMM")
    
    
    cmap = cm.get_cmap('RdYlBu_r')   # Get desired colormap
    color_ratio = np.log(n)/np.log(np.max(n))
    for c, p in zip(color_ratio, patches):
        plt.setp(p, 'facecolor', cmap(c))
    
    plt.show()
    
    plt.savefig('GMM_repartition_histo.png',format = 'png', dpi = 300) #quality = 95 )

    
# flat_histo_3d(x,y,H)  
# histo_3d(x,y,H,xedges,yedges)
histo_2d(x,y)
