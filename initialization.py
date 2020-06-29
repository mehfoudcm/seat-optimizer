import sys
import pandas as pd
import numpy as np
import ast
import os
from os import path
from os import listdir
from pulp import LpVariable, LpProblem, lpSum, LpMaximize, LpBinary, value
import matplotlib.pyplot as plt
from create_clumps import create_clumps


def initialization(seat_map_df, group_label, clump_size_list, clump_ratio_list):
    
    
    if len(clump_size_list) == 1:
        use_clump_array = False
        clump_size = clump_size_list[0]
        
   
    use_clump_ratio = []
    total = 0
    for perc in clump_ratio_list:
        total = perc + total
        use_clump_ratio.append(total)
    
    if total < 1:
        print("clump_ratio not complete, please have total ratio equal to 1; will run with first clump size")
        clump_size = clump_size_list[0]
        
    # creates the clump dataframe, or the real "list of seats"
    # checking and then pulling seat clump dataframe
    folder_name = "Seating Segments/"
    file_name = 'clump_dataframe_'+group_label
    full_file_name = folder_name+file_name+'.csv'
    
    clump_check_point = False
    for i in listdir(folder_name):
        if file_name+".csv" in i:        
            clump_check_point = True
    
    if clump_check_point:   
        clump_df = pd.read_csv(full_file_name, converters={'seat_set': ast.literal_eval,
                                                           'x_coords': ast.literal_eval,
                                                           'y_coords': ast.literal_eval,
                                                           'section': ast.literal_eval,
                                                           'row': ast.literal_eval})
        print("Seating Segments file found, pulled in")
    else:
        print("Seating Segments file not found, creating the file now")
        clump_df = create_clumps(seat_map_df, clump_size_list, group_label)
    

    return clump_df, clump_size_list, use_clump_ratio