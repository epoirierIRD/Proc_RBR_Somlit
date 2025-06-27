#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 16:11:43 2025

@author: epoirier
"""

import pyrsktools as pyrsk
import numpy as np
from datetime import datetime


# Load your RSK file

def split_rsk_by_day (mrsk_file):
    # mrsk_file is a file containing several days, several somlits
        with pyrsk.RSK(mrsk_file) as rsk:
            rsk.readdata()
        
            # Extract unique dates from the datetime column
            timestamps = rsk.data['timestamp']  # numpy.datetime64 array
           
            dates = np.array([ts.astype('datetime64[D]') for ts in timestamps])
            unique_days = np.unique(dates)
            
            # Loop through each unique day and save a new .rsk file
            for day in unique_days:
                # Get mask for rows matching this day
                # mask says true or false if the date is in unique_day
                mask = dates == day
                # completely new copy of the rsk file
                day_rsk = rsk.copy()
                day_rsk.data = rsk.data[mask]  # Filtered data
            
                # Construct filename
                day_str = str(day).replace('-', '')
                #filename = f"split_{day_str}.rsk"
            
                # Save the new RSK file
                day_rsk.RSK2RSK(suffix=day_str)
                print(f"Saved: {day_str}")

# Load the RSK file
mrsk_file = "/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/summer_2024/temp/231853_20240806_1338 somlit25à29.rsk"

split_rsk_by_day (mrsk_file)