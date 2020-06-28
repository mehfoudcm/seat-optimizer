import sys
import pandas as pd
import numpy as np
import ast
import os
from os import path
from os import listdir
import matplotlib.pyplot as plt


def print_map(full_seat_map_df, final_seat_map_df, num_of_seats, percap, method):
    
    plt.clf()
    fig=plt.figure(figsize = (38.40,21.60))
    ax=fig.add_axes([0,0,1,1])
    ax.scatter(full_seat_map_df.seat_center_y, full_seat_map_df.seat_center_x, color='r')
    ax.scatter(final_seat_map_df.seat_center_y, final_seat_map_df.seat_center_x, color='b')
    ax.set_title(f'simple seat map based on the algorithm showing {num_of_seats:d} at {percap:0.2f}% capacity', fontsize = 100)
    plt.savefig('Images/stadium_map_'+method+'.png', bbox_inches='tight', dpi = 300)
    plt.clf()
    return_string = 'Image Saved, '+str(num_of_seats)+' seats filled at '+str(round(percap,2))+'% capacity'
    
    return return_string
