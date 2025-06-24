#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 09:59:06 2025

@author: epoirier
"""


import pyrsktools as pyrsk
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import RSKsomlit_plt as rsksplt
import RSKsomlit_proc as rsksproc
import sensor_uncertainties as sun
from datetime import datetime
from collections import namedtuple
import pandas as pd

# Load the RSK file
mrsk_file = "/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/summer_2024/temp/231853_20240806_1338 somlit25à29.rsk"

'''
with pyrsk.RSK(mrsk_file) as rsk:
       
        # read the data first
        rsk.readdata()
        # tstart = np.datetime64("2024-07-03")
        # tend = np.datetime64("2024-07-25")
        # rsk.readprocesseddata(tstart, tend)
        # print(rsk)
'''


# function to process mrsk file, it means a rsk file containing multiple somlit in it
# corresponding with several profiles and several days: one each day
def split_rsk_file(mrsk_file):
    with pyrsk.RSK(mrsk_file) as rsk:
       
        # read the data first
        rsk.readdata()
        # initiate variable dataframe containing profile nb start and end
        columns = ['profile_nb', 'start_dt', 'end_dt']
        # Create an empty DataFrame with those columns
        df = pd.DataFrame(columns=columns)

        for n in range(len(rsk.regions)):
            if rsk.regions[n].type == 'PROFILE':
               
                df.loc[len(df)] = [n, rsk.regions[n].tstamp1, rsk.regions[n].tstamp2]
                print (type(rsk.regions[n].tstamp1))
               
                # beware the trim removes the data in the range
                
                print(df)
              
                continue
        
        for i in df.index:
            print(df.loc[i])
            if i == 0:
               rsk.trim(reference = 'time', range=[np.datetime64(df.iloc[i+1]['start_dt']), np.datetime64(df.iloc[-1]['end_dt'])], action = 'Nan')
               print(rsk)
            elif i == len(df)-1:
               rsk.trim(reference = 'time', range=[np.datetime64(df.iloc[0]['start_dt']), np.datetime64(df.iloc[-2]['end_dt'])], action = 'remove') 
               print(rsk)
            else:
               rsk.trim(reference = 'time', range=[np.datetime64(df.iloc[0]['start_dt']), np.datetime64(df.iloc[i-1]['end_dt'])], action = 'remove')
               rsk.trim(reference = 'time', range=[np.datetime64(np.datetime64df.iloc[i+1]['start_dt']), np.datetime64(df.iloc[-1]['end_dt'])], action = 'remove')
               print(rsk)
               continue
           
            return df
    
               
'''               
        
        for k in len(liste_profiles):
            if k = 0:
               rsk.trim(reference = 'time', range=[liste_profiles[k][1], action = 'remove') 
        
                if len(liste_profiles) = 1:
                    rsk.trim(reference = 'time', range=[rsk.regions[n].tstamp2,rsk.regions[n].tstamp2], action = 'remove')
                rsk.trim(reference = 'time', range=[rsk.regions[n].tstamp1,rsk.regions[n].tstamp2], action = 'remove')
                rsk.trim(reference = 'time', range=[rsk.regions[n].tstamp1,rsk.regions[n].tstamp2], action = 'remove')
                
                
                # convert the object from np datetime to py datetime
                np_dt = rsk.regions[n].tstamp1
                py_dt = np_dt.astype('datetime64[D]').astype(object)
                # Format as YYYYMMDD to use it in the file name
                date = py_dt.strftime("%Y%m%d")
                rsk.RSK2RSK(outputDir = os.path.dirname(mrsk_file),
                            suffix = date) #we use the date of the profile to rename the rsk
                print(rsk.regions)
                continue
'''            

df = split_rsk_file(mrsk_file)
  
    
'''
# Convert timestamps to just date
rsk.data['date'] = rsk.data['tstamp'].dt.date

# Get unique dates in the file
unique_dates = rsk.data['date'].unique()

# Create output folder
os.makedirs("split_by_day", exist_ok=True)

# Loop over each date and save a new RSK
for date in unique_dates:
    # Filter data for that day
    rsk_day = rsktools.RSK()
    rsk_day.data = rsk.data[rsk.data['date'] == date].copy()
    rsk_day.channels = rsk.channels
    rsk_day.logger = rsk.logger

    # Save as new RSK file
    out_file = f"split_by_day/{date}.rsk"
    rsk_day.writersk(out_file)
    print(f"Saved: {out_file}")
'''