import sys
import pandas as pd
import numpy as np
import ast
import os
from os import path
from os import listdir
import matplotlib.pyplot as plt

"""
Input is the seating CSVs, the full seat map and the optimal seat map (final_seat_map_df), output is the printed image, very basic

"""

def print_map(full_seat_map_df, final_seat_map_df, num_of_seats, percap, method):
    
    plt.clf()
    # set figure size, this is a very big size so that the individual seats can be zoomed in on
    fig=plt.figure(figsize = (38.40,21.60))
    ax=fig.add_axes([0,0,1,1])
    
    # background or base layer, with red showing ALL seats
    ax.scatter(full_seat_map_df.seat_center_y, full_seat_map_df.seat_center_x, color='r')
    # foreground or layer of interest, with blue showing the optimized seat locations
    ax.scatter(final_seat_map_df.seat_center_y, final_seat_map_df.seat_center_x, color='b')
    
    # printing the title with only the simple information required
    ax.set_title(f'simple seat map based on the algorithm showing {num_of_seats:d} at {percap:0.2f}% capacity', fontsize = 80)
    
    # additional implementation of image size and detail, larger than 300 runs into issues when running on Windows
    # saves image to Images folder
    plt.savefig('Images/stadium_map_'+method+'.png', bbox_inches='tight', dpi = 300)
    plt.clf()
    
    # creates the string indicating the completion of the script and image saved
    return_string = 'Image Saved, '+str(num_of_seats)+' seats filled at '+str(round(percap,2))+'% capacity'
    
    return return_string
