import sys
import pandas as pd
import numpy as np
import ast
import os
import time
from os import path
from os import listdir
from pulp import LpVariable, LpProblem, lpSum, LpMaximize, LpBinary, value, PULP_CBC_CMD
import matplotlib.pyplot as plt

"""
This is the code that sets up the optimization (to be done by PuLP), 
taking the distances and clusters and creating the mixed integer linear program

the output is the optimized seats per division
"""

def optimization_setup(distance_df, clump_df, threshold, clump_size_list, clump_ratio_list, group_label, time_limit, top_end_threshold): # , aisle_indicator) #and add aisle indicator
    tic_o = time.perf_counter()
    print("Deleting the single node loops")
    # removing the single node loops, so that optimization runs easier
    delete_index = []
    for i in range(len(distance_df)):
        if distance_df.orig[i] == distance_df.dest[i]:
            delete_index.append(i)
            ######## checking for feasibility
        if distance_df.dist[i] > top_end_threshold:
            delete_index.append(i)
    distance_df = distance_df.drop(index=delete_index)
    distance_df = distance_df.reset_index(drop=True)
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    
    # where ratios are of interest, aka 20% 4 seat clusters 80% 2 seat clusters, these individual nodes need to be created
    print("Creating specific nodes for ratios")
    if len(clump_ratio_list) >= 2:
        nodesA = clump_df[clump_df.clump_size == clump_size_list[0]].seatclumpid.tolist()
        nodesB = clump_df[clump_df.clump_size == clump_size_list[1]].seatclumpid.tolist()
        BAratio = clump_ratio_list[1]/clump_ratio_list[0]
    if len(clump_ratio_list) >= 3:
        nodesC = clump_df[clump_df.clump_size == clump_size_list[2]].seatclumpid.tolist()
        CBratio = clump_ratio_list[2]/clump_ratio_list[1]
    if len(clump_ratio_list) >= 4:
        nodesD = clump_df[clump_df.clump_size == clump_size_list[3]].seatclumpid.tolist()
        DCratio = clump_ratio_list[3]/clump_ratio_list[2]
    if len(clump_ratio_list) >= 5:
        print("optimization method only set up for 4 types of seat clumps and even that can be ridiculous to optimize against")
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    
    print("Creating standard nodes")
    # create the standard list of nodes (seat clumps)
    nodes = clump_df.seatclumpid.tolist()
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    # TODO for aisles if that's something of interest
    #if aisle_indicator == 'no_aisle_seats' or aisle_indicator == 'force_aisle_seats':
    #print("Creating the aisles")
    # create the standard node aisle indicators
    #aisles = dict(zip(clump_df.seatclumpid, clump_df.aisle_clump))
    #toc_o_c = time.perf_counter()
    #print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    
    print("Creating the dictionary for nodes")
    # create a dictionary for those nodes and their value (clump size)
    # their value is not currently set up in a list, this might need to change DELETE IF NOT?
    sizes = dict(zip(clump_df.seatclumpid, clump_df.clump_size))
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    

    print("Creating standard arcs")
    # create a set of nodes to represent arcs (tuple)
    # turn arc set into list
    arcs = distance_df.arc_set.tolist()
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    
    print("Creating the dictionary for arcs")
    # create a dictionary of those sets with distances
    dists = dict(zip(distance_df.arc_set, distance_df.dist))
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    
    print("Creating the variables for acrcs and nodes")
    # OPTIMIZATION MODEL BEGINS
    # Creates the Variables as Integers
    arcvars = LpVariable.dicts("Arc",arcs,0,1,LpBinary)
    nodevars = LpVariable.dicts("Node",nodes,0,1,LpBinary)

    # creates a heavier optimization problem, but allows the flexibility of 2 vs 3 or 3 vs 4 seat clusters
    print("Creating the variables for specific nodes for ratios")
    if len(clump_ratio_list) >= 2:
        nodeAvars = LpVariable.dicts("NodeA",nodesA,0,1,LpBinary)
        nodeBvars = LpVariable.dicts("NodeB",nodesB,0,1,LpBinary)        
    if len(clump_ratio_list) >= 3:
        nodeCvars = LpVariable.dicts("NodeC",nodesC,0,1,LpBinary)
    if len(clump_ratio_list) >= 4:
        nodeDvars = LpVariable.dicts("NodeD",nodesD,0,1,LpBinary)
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    
    print("Initializing the MIP")
    # Creates the 'prob' variable to contain the problem data    
    prob = LpProblem("Maximum Capacity Problem", LpMaximize)

    print("Setting up the objective function")
    # Creates the objective function
    # here's where we would implement weighting for specific seats
    prob += lpSum([nodevars[n]* sizes[n] for n in nodes]), "Total Capacity"
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    
    
    print("Setting up the first set of constraints, arcs = must exist between two nodes that exist")
    # Constraint set #1: insuring that if two nodes exist, the arc between them must exist    
    for j in nodes:    
        for k in nodes:
            if j != k:
                try:
                    prob += 1 + arcvars[(j,k)] >= nodevars[k]+nodevars[j]
                except KeyError:
                    pass
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    
    
    print("Setting up the second set of constraints, arcs can only exist if they're longer than the threshold")
    # Constraint set #2: each arc used must have a distance greater than the threshold
    for a in arcs:
        prob += arcvars[a]*dists[a] >= threshold*arcvars[a]
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    
    print("Setting up the third set of constraints, nodes must exist in both the specific listing and the standard listing if specific arc required for ratio")
    # Constraint set #3: only if there are multiple clump sizes required, make sure they correspond to the typical nodes
    if len(clump_ratio_list) >= 2:
        for a in nodesA:
            prob += nodeAvars[a] == nodevars[a]
        for b in nodesB:
            prob += nodeBvars[b] == nodevars[b]
    if len(clump_ratio_list) >= 3:
        for c in nodesC:
            prob += nodeCvars[c] == nodevars[c]
    if len(clump_ratio_list) >= 4:
        for d in nodesD:
            prob += nodeDvars[d] == nodevars[d]
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    if len(clump_ratio_list) >= 2:
        print("Setting up the fourth set of constraints, the number of arcs in a specific set must fall between 10% of the previous node")
    # Constraint set #4: make sure the ratios of clumps align with what's requested, window of 10%ish
    # window reduced to one constraint per option, indicating that if the number of cluster is increasing
    # it will head for that upper bound as it is more efficient
    if len(clump_ratio_list) >= 2:
        prob += lpSum([nodeBvars[n] for n in nodesB]) <= lpSum([nodeAvars[n] for n in nodesA])*1.1*BAratio
        #prob += lpSum([nodeBvars[n] for n in nodesB]) >= lpSum([nodeAvars[n] for n in nodesA])*0.9*BAratio
    if len(clump_ratio_list) >= 3:
        prob += lpSum([nodeCvars[n] for n in nodesC]) <= lpSum([nodeBvars[n] for n in nodesB])*1.1*CBratio
        #prob += lpSum([nodeCvars[n] for n in nodesC]) >= lpSum([nodeBvars[n] for n in nodesB])*0.9*CBratio
    if len(clump_ratio_list) >= 4:
        prob += lpSum([nodeDvars[n] for n in nodesD]) <= lpSum([nodeCvars[n] for n in nodesC])*1.1*DCratio
        #prob += lpSum([nodeDvars[n] for n in nodesD]) >= lpSum([nodeCvars[n] for n in nodesC])*0.9*DCratio
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    # TODO if aisles are indicated as a point of interest
    #if aisle_indicator == 'no_aisle_seats':
    #print("Setting up the fifth set of constraints, inclusion or exclusion of aisle seats")
    # Constraint set #4: make sure the ratios of clumps align with what's requested, window of 10%ish
    # window reduced to one constraint per option, indicating that if the number of cluster is increasing
    # it will head for that upper bound as it is more efficient
    #for n in nodes:
    #    prob += nodesvars[n]*aisles[n] == 0
    
    #if aisle_indicator == 'force_aisle_seats': not sure this is possible, don't uncomment before finding a reason to move forward here
    #print("Setting up the fifth set of constraints, inclusion or exclusion of aisle seats")
    # Constraint set #4: make sure the ratios of clumps align with what's requested, window of 10%ish
    # window reduced to one constraint per option, indicating that if the number of cluster is increasing
    # it will head for that upper bound as it is more efficient
    #for n in nodes:
    #    prob += nodesvars[n]*aisles[n] ?????
    
    #toc_o_c = time.perf_counter()
    #print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    
    
    
    print("Writing the LP or MPS file now")
    # The problem data is written to an lp or mps file
    # this file can be run on the NEOS server or other optimization servers if you're facing timeout issues or low compute abilities
    prob.writeLP("LP Files/stadium_MCP"+group_label+".lp")
    #prob.writeLP("MPS files/stadium_MCP"+group_label+".mps")
    toc_o_c = time.perf_counter()
    print(f"... {toc_o_c-tic_o:0.4f} seconds have elapsed")
    
    # The problem is solved using PuLP's choice of Solver
    prob.solve(PULP_CBC_CMD(maxSeconds = time_limit, msg = 1, fracGap=0.01))
    # The optimised objective function value is printed to the screen    
    output_val = value(prob.objective)
    print("Total Capacity = ", output_val)
    
    # creates the variables indicating that those clusters were in fact chosen in the optimal list
    TOL = 0.01
    node_ind = []
    for n in nodes:
        if nodevars[n].varValue > TOL:
            node_ind.append(1)
        else:
            node_ind.append(0)

    clump_df['clump_ind'] = node_ind
    
    clump_sum_df = clump_df[['clump_size', 'clump_ind']]
    clump_sum_df = clump_sum_df.groupby(['clump_size']).sum().reset_index()
    
    # creating a size dataframe to understand the final clusters and final cluster ratios
    clump_size_for_df = []
    clump_amount_for_df = []
    for i in range(len(clump_sum_df)):
        clump_size_for_df.append("clusters of "+str(clump_sum_df.clump_size[i]))
        clump_amount_for_df.append(clump_sum_df.clump_ind[i])
        
    size_df = pd.DataFrame([clump_amount_for_df], columns = clump_size_for_df)

    # saves the optimized seats to the Optimized Seats folder so that optimization does not have to run again
    group_item_name = 'group_label_'+group_label+'_opt_seats'
    clump_df.to_csv('Optimized Seats/'+group_item_name+'.csv')
    
    # prints and returns the optimization time, important for experimentation and evolution
    toc_o = time.perf_counter()
    opt_time_num = round(toc_o-tic_o,2)
    print(opt_time_num)
    opt_time = group_label+f" took {toc_o-tic_o:0.4f} seconds\n"
    print(f"Total Optimization for "+opt_time+f" or {(toc_o-tic_o)/60:0.1f} minutes with tolerance")
    
    return opt_time, opt_time_num, output_val, clump_df, size_df
