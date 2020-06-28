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
from initialization import initialization 
from optimization_setup import optimization_setup
from clump_distance import clump_distance
from run_optimization_aggregate import run_optimization_aggregate
from linear_seat_creator import linear_seat_creator
from return_statement_calc import return_statement_calc


def reduced_capacity_seat_creator(file_name, 
                                  threshold = 36,
                                  clump_size_list = [2], 
                                  clump_ratio_list = [1],
                                  algorithm_breakdown = 'section',
                                  time_limit = 1200,
                                  order_direction = 'normal',
                                  top_end_threshold = 150,
                                  #aisle_indicator = 'no_aisle_seats'
                                  clump_size_determination = 'standard',
                                  seat_distance = 12):

    tic = time.perf_counter()
    # bring in full arena or stadium CSV

    
    print("file name = ", file_name)
    print("threshold = ", threshold)
    print("clump_size_list = ", clump_size_list)
    print("clump_ratio_list = ", clump_ratio_list)
    print("time_limit = ", time_limit)
    
    
    ## download the file for seat map
    full_seat_map_df = pd.read_csv(file_name)
    full_seat_map_df['seatsid'] = full_seat_map_df['seatsid'].str.replace('-','')


    if order_direction != 'normal':
        folder_name = "Row Adjusted Arena/"
        file_name = 'full_seat_map_enhanced_df'
        full_file_name = folder_name+file_name+'.csv'
        
        seat_row_check_point = False
        for i in listdir(folder_name):
            if file_name+".csv" in i:
                seat_row_check_point = True
        
        if seat_row_check_point:
            full_seat_map_df = pd.read_csv(full_file_name)
            print("Re-Row/Seat file found, pulled in")
        else:
            print("adjusting seat order and rows based on seat proximity and not order")
            full_seat_map_df = linear_seat_creator(full_seat_map_df, seat_distance)
    
    # setting the indicator column for the seat map dataframe
    # remove if building piece by piece 
    full_seat_map_df['seat_ind'] = [0]*len(full_seat_map_df)

    print("Starting breakdown by "+algorithm_breakdown)
    if algorithm_breakdown == 'section':
        grouping = 'section_label'
    
    if algorithm_breakdown == 'venue':
        grouping = 'venuesid'
    
    # create the list of groups
    group_list = full_seat_map_df[grouping].unique()
    print(group_list)
 
    opt_times = ""
    group_label_array = []
    opt_time_array = []
    total_seats = []
    seats_filled = []
    # algorithm begins here, by segment established in the algorithm breakdown
    # default is section, so it will create a map, section by section
    for group_label in group_list:
        
        print("Creating seating segments now for ", group_label)
        group_seat_map_df = full_seat_map_df[full_seat_map_df[grouping] == group_label]
        group_label = str(group_label)
        clump_df, clump_size_list, use_clump_ratio = initialization(group_seat_map_df, group_label, clump_size_list, clump_ratio_list)

        total_seats = np.append(total_seats,len(clump_df))
            
        print("Checking for distances for ", group_label)
        # creates the clump dataframe, or the real "list of seats"
        # checking and then pulling seat clump dataframe
        folder_name = "Distances/"
        file_name = 'group_label_'+group_label+'_dist'
        full_file_name = folder_name+file_name+'.csv'
    
        dist_check_point = False
        for i in listdir(folder_name):
            if file_name+".csv" in i:        
                dist_check_point = True
    
        if dist_check_point:   
            distance_df = pd.read_csv(full_file_name)
            distance_df.arc_set = distance_df.arc_set.apply(ast.literal_eval)
            print("Distances file found, pulled in")
        else:
            print("Distances file not found, creating the file now")
            distance_df = clump_distance(clump_df, group_label)
        
        # RUNNING THE OPERATIONS TO PRODUCE THE SEATS 
        
        
        print("Checking for optimized files for ", group_label)
        folder_name = "Optimized Seats/"
        file_name = 'group_label_'+group_label+'_opt_seats'
        full_file_name = folder_name+file_name+'.csv'
        
        opt_check_point = False
        for i in listdir(folder_name):
            if file_name+".csv" in i:
                opt_check_point = True
        
        if opt_check_point:
            clump_df_opt_group = pd.read_csv(full_file_name)
            opt_time = str(group_label+ " optimization already handled\n")
            opt_time_num = 0
            output_val = len(clump_df_opt_group[clump_df_opt_group.clump_ind == 1])
            print("Optimized Seats file found, pulled in")
        else:
            print("Optimized Seats file not found, creating the file now")
            opt_time, opt_time_num, output_val, clump_df_opt_group = optimization_setup(distance_df, clump_df, threshold, clump_size_list, clump_ratio_list, group_label, time_limit, top_end_threshold) #, aisle_indicator)
        
        seats_filled = np.append(seats_filled, output_val)
        group_label_array = np.append(group_label_array, group_label)
        opt_time_array = np.append(opt_time_array, opt_time_num)
        
        
        opt_times = opt_times + opt_time
        print("\n Current Optimization Times:\n"+opt_times+"\n")
        #clump_df_opt_group = optimization_setup(distance_df, clump_df, threshold, clump_size_list, clump_ratio_list, group_label)
        print("Establishing the full seat map using optimized files for ", group_label)
        full_seat_map_df = run_optimization_aggregate(clump_df_opt_group, full_seat_map_df, opt_check_point)
        

        print("\n\n\n  Nearly "+str(round(len(group_label_array)*100/len(group_list),2))+"% completed \n\n\n")
    
    print("Begin aggregation and map creation of all groupings")
    return_opt = return_statement_calc(full_seat_map_df, 'opt')

    runtime_df = pd.DataFrame({'group label': list(group_label_array), 'total seats': list(total_seats), 'seats filled': list(seats_filled)},
                            columns=['group label', 'total seats', 'seats filled'])
    runtime_df['opt_time'] = list(opt_time_array)
    runtime_df.to_csv('optimization_runtime.csv')
    toc = time.perf_counter()
    timing = f"... took {toc-tic:0.4f} seconds or {(toc-tic)/60:0.1f} minutes"
    return print(return_opt, timing)






file_name = sys.argv[1]
threshold = ast.literal_eval(sys.argv[2])
clump_size_list = ast.literal_eval(sys.argv[3])
clump_ratio_list = ast.literal_eval(sys.argv[4])
algorithm_breakdown = sys.argv[5]
time_limit = ast.literal_eval(sys.argv[6])
order_direction = sys.argv[7]
#aisle_indicator = sys.argv[8] # and add it below


if __name__ == "__main__":
    reduced_capacity_seat_creator(file_name, threshold, clump_size_list, clump_ratio_list, algorithm_breakdown, time_limit, order_direction)
