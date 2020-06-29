import sys
import pandas as pd
import numpy as np
import ast
import os
from os import path
from os import listdir

"""
This is the distance function used to create the distance array
Runs the necessary (n^2)/2 calculations requested by clump_distance function

possible for the function to hit errors if any of the coordinates are not integers or floats

- looks through each x coordinate and y coordinate of the first cluster 
  and then calculates the distance from each of the x,y points of the second cluster
  
- then from that list of distances, 
    the minimum distance is then output as the distance between those two clusters
"""

def distance_fun(clump_df,i,j):
    dist_list = []
    for w in clump_df.x_coords[i]:
        for x in clump_df.y_coords[i]:
            for y in clump_df.x_coords[j]:
                for z in clump_df.y_coords[j]:
                    dist_list.append(np.sqrt((y-w)**2+(z-x)**2))
    return np.min(dist_list)
