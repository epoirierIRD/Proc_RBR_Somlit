#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 16:41:22 2025

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

'''
# ------------------------------------MAIN-------------------------------------
# 
# Main
# pc path of rsk file
path_in = "/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240606/231853_20240607_1104 somlit 21.rsk"
# Get the directory of main.py situated next to rsk file
path_out = os.path.dirname(os.path.abspath(__file__))


# enter parameters somlit point id and atmospheric pressure 
site_id = 5
patm = 10.1325 #dBar

# list of parameters in the rsk file that we want in the csv to export
# do not choose pressure, sea_pressure and depth, it does not work
# might be to have an alert between parameters in the rsk and parameters we want to save:
    # you cannot export parameters in csv if they are not in the rsk
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

# calling processing function, we use the rsk object that has the same id as rsk_u and rsk_d processed files
raw,rsk,rsk_d,rsk_u, profile_nb,file_output_folder,csv_d,csv_u = rsksproc.procRSK (path_in, patm, site_id, param, path_out)

# Plot with loop on parameters except unworking ones
# figures stored in appropriate directory
# we exclude here reference channels
exclude = ['pressure','sea_pressure','depth']
for param in [ x for x in param if x not in exclude] :
       
    
    # Plot up and down casts processed on the same graph with uncertainties
    rsksplt.plot_up_down2(rsk_d, rsk_u, param, profile_nb, file_output_folder)

# Code an option if we want to choose the upward profile instead of the downward

# Exporting to SOMLIT csv file format
# function to convert the upcast and downcast csv files into the good format csv for SOMLIT DB
# one file per cast downward and upward and stored in dedicated downcast and upcast folders

# below is the loop on the rsk files not used at the moment,
# but still working on one file
'''
rsksproc.process_rsk_folder(
    path_in="/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240606/",
    path_out="/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240606/",
    site_id=5,
    patm = 10.1325,
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





