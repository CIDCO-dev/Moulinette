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
from sklearn.utils.class_weight  import compute_class_weight 
#import statistics as st



def weight_based_truncature(df):
    ligne_a_suppr = []
    arr =  df['Nbrs_Moules'].values
    classes = np.unique(arr)
    weight_list = compute_class_weight(
                                        class_weight = 'balanced',
                                        classes = np.unique(arr) ,
                                        y = arr
                                       )### This alternative synthesis is necessary due to a known bug in compute_class_weight()
    ratio_list = 1/weight_list
    
    for i in range(len(ratio_list)):
        ratio = ratio_list[i]
        if ratio > 1:
            df_1 = df.loc[df['Nbrs_Moules']==classes[i]]
            n = len(df_1)
            if n < ratio:
                ligne_a_suppr = np.append(ligne_a_suppr, df_1.index.values[1:])
            else:
                keeping = int(n//ratio)
                ligne_a_suppr = np.append(ligne_a_suppr, df_1.index.values[keeping:])
    df = df.drop(ligne_a_suppr)
    df = df.reset_index(drop = True)
    
    return df
                
        

def freq_max_based_truncature(df,freq_max):
    ligne_a_suppr = []
    nbrs_moules = df['Nbrs_Moules']
    frequency = np.bincount(nbrs_moules)
    for i in range(len(frequency)):
        ratio = frequency[i]/freq_max
        if ratio > 1:
            df_1 = df.loc[df['Nbrs_Moules'] == i]
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
    
    return df            
                

     
def plot_histo(df):
    z = df['Nbrs_Moules'].values
    plt.figure()
            
    n, bins, patches = plt.hist(z,np.arange(max(z)+1), color = 'g', edgecolor = 'black')  
    
    plt.xticks(np.arange(110, step = 10))
    #plt.xlim(0, max(z) + 1)
    plt.xlabel("Nombres de moules")
    plt.ylabel("Nbrs de points mbes")
    plt.title("Histogramme de répartition des moules")
    
    
    cmap = cm.get_cmap('RdYlBu_r')   # Get desired colormap
    color_ratio = np.log(n)/np.log(np.max(n))
    for c, p in zip(color_ratio, patches):
        plt.setp(p, 'facecolor', cmap(c))


# def stats(df):
#     sample = df['Nbrs_moules'].values
    
#     print(f"repartition: {np.bincount(sample)}")
#     print(f"weight: {class_weight.compute_class_weight('balanced', np.unique(sample) ,sample)}")

    
#     print(f"moyenne: {st.mean(sample)}")
#     #print(f"Geometric mean of data: {st.geometric_mean(sample)}")
#     print(f"Harmonic mean of data: {st.harmonic_mean(sample)}")
#     print(f"Median (middle value) of data: {st.median(sample)}")
#     print(f"Low median of data: {st.median_low(sample)}")
    
#     print(f"High median of data: {st.median_high(sample)}")
#     print(f"Median, or 50th percentile, of grouped data: {st.median_grouped(sample)}")
#     print(f"Single mode (most common value) of discrete or nominal data: {st.mode(sample)}")
#     print(f"List of modes (most common values) of discrete or nominal data: {st.multimode(sample)}")
    
    
#     print(f"eDivide data into intervals with equal probability: {st.quantiles(sample)}")
#     print(f"Population standard deviation of data: {st.pstdev(sample)}")
#     print(f"Population variance of data: {st.pvariance(sample)}")
#     print(f"Sample standard deviation of data: {st.stdev(sample)}")
#     print(f"Sample variance of data: {st.variance(sample)}")

################################################################################
# Main                                                                         #
################################################################################

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #  	sys.stderr.write("Usage: remove_overrepresented.py training_data.txt maximum_frequency_allowed \n")
    #  	sys.exit(1)
     	
    # filename = sys.argv[1]
    # freq_max = int(sys.argv[2])
    
    filename = "C:\\Users\Hydrograhe\Documents\\GitHub\\Moulinette\\data\\training_data_5m.txt"
    
    freq_max = 80
    
    df = pd.read_csv(filename, delimiter = '\s+', header = 0)
    
    # df_1 = freq_max_based_truncature(df,ligne_a_suppr,freq_max)
    # df_2 = weight_based_truncature(df,ligne_a_suppr)
    
    plot_histo(df)
    # plot_histo(df_1)
    # plot_histo(df_2)
    
    #stats(df)
    
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width',None):  # more options can be specified also
    #     print(df_1.to_string(index=False))
    
    	
    
    


	


	



	



	




	



	





