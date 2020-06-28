import pandas as pd
import numpy as np
import time

def linear_seat_creator(df, seat_distance):
    tic_l = time.perf_counter()
    full_seat_map_df_enhanced = df
    full_seat_map_df_enhanced['unique_indicator'] = [None]*len(full_seat_map_df_enhanced)

    for i in range(len(full_seat_map_df_enhanced)):
        full_seat_map_df_enhanced.unique_indicator[i] = str(full_seat_map_df_enhanced.section_label[i]) + str(full_seat_map_df_enhanced.row_label[i])

    row_list = list(full_seat_map_df_enhanced.unique_indicator.unique())

    for row in row_list:
        new_row_df = full_seat_map_df_enhanced[full_seat_map_df_enhanced.unique_indicator == row]
        new_row_df = new_row_df.reset_index(drop=True)
        new_row_df['new_seat_number']= [0]*len(new_row_df)
        min_x = np.min(new_row_df.seat_center_x)
        if len(new_row_df[new_row_df.seat_center_x == min_x])>1:
            min_y = np.min(new_row_df.seat_center_y)
            ##if min_x and min_y are not unique, seats are the same,
            ##reconfiguring x and y are needed
            new_row_df.new_seat_number[new_row_df.seat_center_y == min_y] = 1
        else:
            new_row_df.new_seat_number[new_row_df.seat_center_x == min_x] = 1
            
        main_x = new_row_df[new_row_df.new_seat_number == 1].seat_center_x.values[0]
        main_y = new_row_df[new_row_df.new_seat_number == 1].seat_center_y.values[0]
        new_row_df['seat_distance_from_one']= [0]*len(new_row_df)
        for i in range(len(new_row_df)):
            i_x = new_row_df.seat_center_x[i]
            i_y = new_row_df.seat_center_y[i]
            new_row_df.seat_distance_from_one[i] = np.sqrt(((i_x-main_x)**2)+((i_y-main_y)**2))
            print("creating new seat numbers for cluster creation in "+row)
        new_row_df = new_row_df.sort_values(by=['seat_distance_from_one']).reset_index(drop=True)
        
        for i in range(1,len(new_row_df)):
            if new_row_df.seat_distance_from_one[i] - new_row_df.seat_distance_from_one[i-1] > seat_distance*2:
                print("creating new rows for cluster creation, breaks exist in rows in "+row)
                new_row_label = str(new_row_df.row_label[i]) + str(new_row_df.seat_number[i])
                new_unique_indicator = row + str(new_row_df.seat_number[i])
                for j in range(i,len(new_row_df)):

                    full_seat_map_df_enhanced.loc[full_seat_map_df_enhanced.seatsid == new_row_df.seatsid[j], 'row_label'] = new_row_label
                    
                    full_seat_map_df_enhanced.loc[full_seat_map_df_enhanced.seatsid == new_row_df.seatsid[j], 'unique_indicator'] = new_unique_indicator


        
                row_list.append(new_unique_indicator)
                

        new_row_df['new_seat_number'] = range(1,len(new_row_df)+1)
        for i in range(len(new_row_df)):
            full_seat_map_df_enhanced.loc[full_seat_map_df_enhanced.seatsid == new_row_df.seatsid[i], 'new_seat_number'] = int(new_row_df.new_seat_number[i])
    
    full_seat_map_df_enhanced = full_seat_map_df_enhanced.rename(columns={'seat_number': 'old_seat_number', 'new_seat_number': 'seat_number'})
    
    
    full_seat_map_df_enhanced.to_csv('Row Adjusted Arena/full_seat_map_enhanced_df.csv')
    
    toc_l = time.perf_counter()
    print(f"Linear Seat Creation took {toc_l-tic_l:0.4f} seconds")
    return full_seat_map_df_enhanced

