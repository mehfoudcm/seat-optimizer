import sys
import pandas as pd
import numpy as np
import ast
import os
from os import path
from os import listdir
from print_map import print_map


def return_statement_calc(full_seat_map_df, method):
    
    final_seat_map_df = full_seat_map_df[(full_seat_map_df.seat_ind == 1)]
    final_seat_map_df.to_csv('Final Seat Map/seat_map_by_groups_final_'+method+'.csv')
    full_seat_map_df.to_csv('Final Seat Map/seat_map_by_groups_full_'+method+'.csv')
    num_of_seats = len(final_seat_map_df)
    capacity = len(full_seat_map_df)
    percap = num_of_seats*100/capacity
    
    final_return = print_map(full_seat_map_df, final_seat_map_df, num_of_seats, percap, method) 
    return final_return 