#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 12:10:26 2025

@author: epoirier
"""

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

path = "/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/summer_2024/temp"


# First we gonna check if there is multiple rsk files, the check if there is duplicate:
# meaning rsk files containing the same data for the same day
# then we have a clear list of rsk files to process

rsksproc.scan_rsk(path)



# Then we will process each rsk file (daily files) one after the other and store the data in dedicated folders
# Next idea is to store the data with the somlit number and date


rsksproc.process_rsk_folder(
    path_in = path,
    site_id =5,
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





