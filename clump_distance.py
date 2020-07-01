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

"""
For the purpose of taking the clumps or clusters of seats created and assigning a distance to each combination

"""


def clump_distance(clump_df, group_label, top_end_threshold):
    tic_d = time.perf_counter() # timing the process
    
    # creating a distance matrix, that runs through the distance function
    dist_matrix = np.zeros((len(clump_df),len(clump_df)))
    k = 0
    for i in range(len(clump_df)):
        for j in range(i):
            dist_matrix[i,j] = distance_fun(clump_df,i,j,top_end_threshold)
            print("clump_distance for "+group_label+" is running", round(2*k/(len(clump_df)**2),3))
            k = k+1
    
    # flips the distance matrix and makes sure each arc has a distance (rather than doing twice the calculations
    dist_matrix = dist_matrix + dist_matrix.T - np.diag(np.diag(dist_matrix))
    
    # turns the distance matrix into a dataframe with three columns
    dist_df = pd.DataFrame(dist_matrix, columns=clump_df.seatclumpid, index = clump_df.seatclumpid2) 
    distance_df = dist_df.stack().reset_index()
    distance_df = distance_df.rename(columns = {'seatclumpid':'orig', 'seatclumpid2':'dest', 0:'dist'}) 
    
    # creates the arc_set of the columns, rather than iteratively going through the process
    distance_df['arc_set'] = list(zip(distance_df.orig, distance_df.dest))
    
    # saves the distance dataframe for each set
    group_item_name = 'group_label_'+group_label+'_dist'
    distance_df.to_csv('Distances/'+group_item_name+'.csv')
    
    toc_d = time.perf_counter() # outputs the time that the distance creation took
    print("Distance Creation for "+group_label+f" took {toc_d-tic_d:0.4f} seconds")
    return distance_df 
