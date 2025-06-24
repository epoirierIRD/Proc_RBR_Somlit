#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 09:47:35 2025

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


rsksproc.process_rsk_file(input_file = "/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240606/231853_20240607_1104 somlit 21.rsk",
                          path_out = os.path.dirname('/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240606/231853_20240607_1104 somlit 21.rsk'),
                          site_id = 5,
                          p_tresh = 0.4,
                          c_tresh = 5,
                          patm = 10.1325, # dBar
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
                                ] )
