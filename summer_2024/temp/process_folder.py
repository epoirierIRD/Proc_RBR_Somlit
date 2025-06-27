#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 13:42:39 2025

@author: epoirier
"""

import pyrsktools as pyrsk
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import pandas as pd
from datetime import datetime
import glob
from pathlib import Path

# custom lib
import sites
import RSKsomlit_proc as rsksproc
import RSKsomlit_plt as rsksplt


# ****************************************************************************************************************
# function to procees a list of rsk files in a chosen folder
# issue at the moment, it works only for the last file I think,
# the loop does not properly work certainly because of the variable of the profle_nb that does not update in the loop.
def process_rsk_folder(path_in, site_id, p_tresh, c_tresh, patm, param):
    
    rsk_files = glob.glob(os.path.join(path_in, "*.rsk")) # creates the list of rsk files
    print('found these RSK files to process' + rsk_files)
    
    
    
    
    
    
    # assuming the rsk files are in a rawdatafolder
    # we want to store the processes_data in a proc_data dir
    parent_dir = os.path.dirname(path_in)    # get the dir a step up
    path_out = os.path.join(parent_dir, "procdata")
    # creates the path_out directory woth proc_data if it don't already exists
    os.makedirs(path_out, exist_ok=True)
    
    rsk_files = glob.glob(os.path.join(path_in, "*.rsk")) # creates the list of rsk files
    print('found these RSK files to process' + rsk_files)
    
    for i, input_file in enumerate(rsk_files): # loop on my list of files
        
        
        
        
        
        
        
        
        print(f"\n--- Processing file {i+1}/{len(rsk_files)}: {input_file} ---")
        rsksproc.process_rsk_file(input_file, path_out, site_id, p_tresh, c_tresh, patm, param)
    
    for input_file in rsk_files:
       rsksproc.process_rsk_file(input_file, path_out, site_id, p_tresh, c_tresh, patm, param)
       
       
       
       
       

rsksproc.process_rsk_folder(
    path_in="/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/summer_2024/temp",
    site_id=5,
    patm = 10.1325,
    p_tresh = 0.4,
    c_tresh = 5,
    param = ['conductivity',
          'temperature',
          #'pressure',
          'temperature1',
          'dissolved_o2_concentration',
          'par',
          'ph',
          'chlorophyll-a',
          'fdom',
          'turbidity',
          # 'sea_pressure',
          'depth',
          'salinity',
          # 'speed_of_sound',
          # 'specific_conductivity',
          # 'dissolved_o2_saturation',
          # 'velocity',
          'density_anomaly'
          ]
)

       