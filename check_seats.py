from os import path
from os import listdir
import sys
import pandas as pd
from distance_fun import distance_fun
import ast
import time

"""
for the purpose of adding more material for analysis of the section and the optimization
adds minimum distance in order to insure feasiblity
adds average minimum distance and maximum minimum distance across clusters to understand how successful the optimization was at timeout (if timeout)
"""

def check_seats():
    # timing the process 
    tic = time.perf_counter()
    
    # sets top_end_threshold, can be parameterized, set high so unused
    top_end_threshold = 1000
    
    # sets folder
    optimized_seats = 'Optimized Seats/'
    group_label = []
    overall_min_distance = []
    overall_max_distance = []
    overall_avg_min_dist = []

    # goes through the folder of optimized seats, to perform analysis on each group
    for spec_group in listdir(optimized_seats):
        if 'group_label_' in spec_group:
            group_label.append(spec_group.replace('group_label_','').replace('_opt_seats.csv',''))
    
    
            # reads the specific optimized seats file in and reduces it to only clusters indicated
            df_opt_seats = pd.read_csv(optimized_seats+spec_group)
            df_opt_seats = df_opt_seats[df_opt_seats.clump_ind == 1]
            df_opt_seats = df_opt_seats.reset_index()
            # sets coordinates to be literal list read in
            for i in range(len(df_opt_seats)):
                df_opt_seats.x_coords[i] = ast.literal_eval(df_opt_seats.x_coords[i])
                df_opt_seats.y_coords[i] = ast.literal_eval(df_opt_seats.y_coords[i])
            
            # reads in the distance from each cluster (A) and then uses the distance function
            # to calculate the min distance of every other cluster (B, C, D...) from that initial cluster (A)
            df_opt_seats['min_dist'] = [0]*len(df_opt_seats)
            for ind_seat in range(len(df_opt_seats)):
                seat_distances = []
                for other_seat in range(len(df_opt_seats)):
                    if other_seat != ind_seat:
                        seat_distances.append(distance_fun(df_opt_seats, ind_seat, other_seat, top_end_threshold))
            
                df_opt_seats.min_dist[ind_seat] = min(seat_distances)
        
            # sets up aggregate for calculating measures of that minimum distance of the specific clusters
            overall_min_distance.append(min(df_opt_seats.min_dist))
            overall_max_distance.append(max(df_opt_seats.min_dist))
            overall_avg_min_dist.append(round(sum(df_opt_seats.min_dist)/len(df_opt_seats.min_dist),2))
        
    # puts the list together to create a dataframe
    df_lists = list(zip(group_label, overall_min_distance, overall_max_distance, overall_avg_min_dist))

    seat_check_df = pd.DataFrame(df_lists, columns = ['group label', 'min_distance', 'max_min_distance', 'avg_min_distance'])

    # outputs the time and the dataframe
    toc = time.perf_counter() # outputs the time that the seat check took
    print(f"Seat Check for arena took {toc-tic:0.4f} seconds")
    
    return seat_check_df
