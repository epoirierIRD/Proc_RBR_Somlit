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




rsksproc.process_rsk_folder(
    path_in="/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240130/rawdata",
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





