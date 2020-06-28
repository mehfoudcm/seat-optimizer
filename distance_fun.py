import sys
import pandas as pd
import numpy as np
import ast
import os
from os import path
from os import listdir


def distance_fun(clump_df,i,j):
    dist_list = []
    for w in clump_df.x_coords[i]:
        for x in clump_df.y_coords[i]:
            for y in clump_df.x_coords[j]:
                for z in clump_df.y_coords[j]:
                    dist_list.append(np.sqrt((y-w)**2+(z-x)**2))
    return np.min(dist_list)