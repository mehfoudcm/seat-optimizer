import sys
import pandas as pd
import numpy as np
import ast
import os
from os import path
from os import listdir
import time
from pulp import LpVariable, LpProblem, lpSum, LpMaximize, LpBinary, value
import matplotlib.pyplot as plt
from distance_fun import distance_fun

def clump_distance(clump_df, group_label):
    tic_d = time.perf_counter()
            
    dist_matrix = np.zeros((len(clump_df),len(clump_df)))
    k = 0
    for i in range(len(clump_df)):
        for j in range(i):
            dist_matrix[i,j] = distance_fun(clump_df,i,j)
            print("clump_distance for "+group_label+" is running", round(2*k/(len(clump_df)**2),3))
            k = k+1
    
    dist_matrix = dist_matrix + dist_matrix.T - np.diag(np.diag(dist_matrix))
    dist_df = pd.DataFrame(dist_matrix, columns=clump_df.seatclumpid, index = clump_df.seatclumpid2) 
    
    distance_df = dist_df.stack().reset_index()
    distance_df = distance_df.rename(columns = {'seatclumpid':'orig', 'seatclumpid2':'dest', 0:'dist'}) 
    
    distance_df['arc_set'] = list(zip(distance_df.orig, distance_df.dest))
    
    
    group_item_name = 'group_label_'+group_label+'_dist'
    distance_df.to_csv('Distances/'+group_item_name+'.csv')
    
    toc_d = time.perf_counter()
    print("Distance Creation for "+group_label+f" took {toc_d-tic_d:0.4f} seconds")
    return distance_df 
