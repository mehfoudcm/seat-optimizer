import sys
import pandas as pd
import numpy as np
import ast
import os
from os import path
from os import listdir

"""
for the purpose of aggregating the optimized seat map of clusters and indicating the seats that correspond
"""

def run_optimization_aggregate(clump_df_opt_group, full_seat_map_df, opt_check_point):
    # takes the seats in an optimal cluster and add it to the final seat list 
    final_seat_list = []
    # if it comes from the csv
    if opt_check_point:
        for i in range(len(clump_df_opt_group)):
            if clump_df_opt_group.clump_ind[i] == 1:
                final_seat_list.extend(ast.literal_eval(clump_df_opt_group.seat_set[i]))
    # if it is created just then (dealing with difficulties in formating of CSVs and consumption
    else:
        for i in range(len(clump_df_opt_group)):
            if clump_df_opt_group.clump_ind[i] == 1:
                final_seat_list.extend(clump_df_opt_group.seat_set[i])


    # if the seats are in the final seat list, add them to the full seat map
    for i in range(len(full_seat_map_df)):
        if full_seat_map_df.seatsid[i] in final_seat_list:
            full_seat_map_df.seat_ind[i] = 1

    # print an in_progress csv showing what sections have been completed if stopping is desired
    full_seat_map_df.to_csv('Final Seat Map/seat_map_by_groups_in_progress_opt.csv')

    
    return full_seat_map_df
