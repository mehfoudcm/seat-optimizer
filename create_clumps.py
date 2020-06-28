import sys
import pandas as pd
import numpy as np
import ast
import os
import time
from os import path
from os import listdir
from pulp import LpVariable, LpProblem, lpSum, LpMaximize, LpBinary, value
import matplotlib.pyplot as plt

def create_clumps(df, clump_size_list, group_label, order_direction = 'normal'):
    tic_c = time.perf_counter()
    final_clump_df = pd.DataFrame(columns=['seat_set', 'x_coords','y_coords','section','row'])

    for clump_size in clump_size_list:
        clumps = []
        rows_in_section = df.row_label.unique()
        for i in rows_in_section:
            row_df = df[df.row_label == i]
            if order_direction == 'normal':
                min_seat = int(min(row_df.seat_number))
                max_seat = int(max(row_df.seat_number))
                for j in range(min_seat,max_seat-(clump_size-1)+1):
                    # add in indicator for aisle
                    #if j == min_seat or j == max_seat-(clump_size-1)+1:
                        #aisle_clump = 1 # then add aisle_clump to append below
                    seat_set = []
                    seat_x_set = []
                    seat_y_set = []
                    seat_section = []
                    seat_row = []
                    for k in range(0, clump_size):
                        try:
                            seat_set.append(row_df[row_df.seat_number == j+k].iloc[0]['seatsid'])
                            seat_x_set.append(row_df[row_df.seat_number == j+k].iloc[0]['seat_center_x'])
                            seat_y_set.append(row_df[row_df.seat_number == j+k].iloc[0]['seat_center_y'])
                            seat_section.append(group_label)
                            seat_row.append(i)
                        except IndexError:
                            #print("reached the end of the row")
                            pass
                    clumps.append([tuple(seat_set), list(seat_x_set), list(seat_y_set), tuple(seat_section), tuple(seat_row)])    


        clump_set = clumps
        clump_df = pd.DataFrame(clump_set, columns=['seat_set', 'x_coords','y_coords','section','row']) 
        
        delete_index = []
        for i in range(len(clump_df)):
            if len(clump_df.seat_set[i]) != clump_size:
                delete_index.append(i)
        clump_df = clump_df.drop(index=delete_index)
        clump_df = clump_df.reset_index(drop=True)


        clump_df['seatclumpid'] = [None]*len(clump_df)
        clump_df['seatclumpid2'] = [None]*len(clump_df)
        clump_df['clump_size'] = [clump_size]*len(clump_df)

        for i in range(len(clump_df)):
            clump_id = ''
            for j in range(clump_size):
                clump_id = clump_id + clump_df.seat_set[i][j]
            clump_df.seatclumpid[i] = clump_id + str(clump_size)
        clump_df.seatclumpid2 = clump_df.seatclumpid
    
        final_clump_df = final_clump_df.append(clump_df)
    
        
    final_clump_df = final_clump_df.loc[:, ~final_clump_df.columns.str.contains('^Unnamed')]
    #final_clump_df[['x_coords', 'y_coords']] = final_clump_df[['x_coords', 'y_coords']].apply(pd.to_numeric)
    final_clump_df = final_clump_df.reset_index(drop=True)
    final_clump_df.to_csv('Seating Segments/clump_dataframe_'+group_label+'.csv')
    
    
    toc_c = time.perf_counter()
    print("Clump Creation for "+group_label+f" took {toc_c-tic_c:0.4f} seconds")
    return final_clump_df
