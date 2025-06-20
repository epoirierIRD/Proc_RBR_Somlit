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


# ------------------------------------MAIN-------------------------------------
# 
# Main
# pc path
path_in = "/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/rawdata/sample.rsk"
# Get the directory of main.py
path_out = os.path.dirname(os.path.abspath(__file__))


# enter parameters of your local processing and somlit point
# must find a way to determine profile nb automatically
patm = 10.1325
latitude = 48.35

# list of parameters in the rsk file
param = ['conductivity',
      'temperature',
      #'pressure',
      'temperature1',
      #'dissolved_o2_concentration',
      #'par',
      #'ph',
      #'chlorophyll-a',
      #'fdom',
      #'turbidity',
      # 'sea_pressure',
      # 'depth',
      'salinity',
      # 'speed_of_sound',
      # 'specific_conductivity',
      # 'dissolved_o2_saturation',
      # 'velocity',
      # 'density_anomaly'
      ]


# calling processing function, we use the rsk object that have the same id as rsk_u and rsk_d processed files
raw,rsk,rsk_d,rsk_u, profile_nb = rsksproc.procRSK (path_in, patm, latitude, param, path_out)

#plotting and choosing the parameters to plot
for param in param:
       
    
    # Plot up and down casts processed on the same graph with uncertainties
    # we can see that the been avergaging is not working on upcast: points are not aligned
    # to be solved 
    rsksplt.plot_up_down2(rsk_d, rsk_u, param, profile_nb, path_out)

    # plot raw and processed data for up and down casts on differents profiles    

    # get the uncertainty for each param to use in the plots below
    # uncertainty = sun.get_uncertainty(param)
       
    # for cast in ['down','up']:
    #     if cast == 'down':
    #         fig1, axes1 = rsksplt.plot_raw_proc(rsk_d, rsk, param, cast, profile_nb, uncertainty)
    #     else:
    #         fig2, axes2 = rsksplt.plot_raw_proc(rsk_u, rsk, param, cast, profile_nb, uncertainty)

# Add here a function to trim de chosen cast up or down once the graphs have been checked
# Code an option if we want to choose the upward profile instead of the downward


# ------
'''
# function to convert the downcast file into the good format for SOMLIT DB
rsksproc.toSomlitDB('/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240606/downcast/231853_20240607_1104 somlit 21_profile0.csv',
                    5, # site_id
                    '/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240606/downcast/4Somlit.csv')

'''


