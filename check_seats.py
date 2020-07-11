from os import path
from os import listdir
import sys
import pandas as pd
from distance_fun import distance_fun
import ast
import time


def check_seats():
    tic = time.perf_counter()
    top_end_threshold = 150
    optimized_seats = 'Optimized Seats\\'
    group_label = []
    overall_min_distance = []
    overall_avg_min_dist = []

    for spec_group in listdir(optimized_seats):
        group_label.append(spec_group.replace('group_label_','').replace('_opt_seats.csv',''))
    
    
    
        df_opt_seats = pd.read_csv(optimized_seats+spec_group)
        df_opt_seats = df_opt_seats[df_opt_seats.clump_ind == 1]
        df_opt_seats = df_opt_seats.reset_index()
    
        for i in range(len(df_opt_seats)):
            df_opt_seats.x_coords[i] = ast.literal_eval(df_opt_seats.x_coords[i])
            df_opt_seats.y_coords[i] = ast.literal_eval(df_opt_seats.y_coords[i])
        
        df_opt_seats['min_dist'] = [0]*len(df_opt_seats)
        for ind_seat in range(len(df_opt_seats)):
            seat_distances = []
            for other_seat in range(len(df_opt_seats)):
                if other_seat != ind_seat:
                    seat_distances.append(distance_fun(df_opt_seats,ind_seat,other_seat, top_end_threshold))
        
            df_opt_seats.min_dist[ind_seat] = min(seat_distances)
    
        overall_min_distance.append(min(df_opt_seats.min_dist))
        overall_avg_min_dist.append(round(sum(df_opt_seats.min_dist)/len(df_opt_seats.min_dist),2))
    
    
    df_lists = list(zip(group_label, overall_min_distance, overall_avg_min_dist))

    seat_check_df = pd.DataFrame(df_lists, columns = ['group label', 'min_distance', 'avg_min_distance'])


    toc = time.perf_counter() # outputs the time that the seat check took
    print(f"Seat Check for arena took {toc-tic:0.4f} seconds")
    
    return seat_check_df