import sys
import pandas as pd
import numpy as np
import ast
import os
from os import path
from os import listdir
from print_map import print_map

"""
for the purpose of returning the visuals/ results

"""


def return_statement_calc(full_seat_map_df, method):
    # creates dataframe of optimal seats only
    final_seat_map_df = full_seat_map_df[(full_seat_map_df.seat_ind == 1)]
    # saves optimal seats and all seats to two separate CSVs
    final_seat_map_df.to_csv('Final Seat Map/seat_map_by_groups_final_'+method+'.csv')
    full_seat_map_df.to_csv('Final Seat Map/seat_map_by_groups_full_'+method+'.csv')
    # simple math on results
    num_of_seats = len(final_seat_map_df)
    capacity = len(full_seat_map_df)
    percap = num_of_seats*100/capacity
    
    # prints and saves seating map
    final_return = print_map(full_seat_map_df, final_seat_map_df, num_of_seats, percap, method) 
    return final_return 
