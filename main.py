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


# ------------------------------------MAIN-------------------------------------
# 
# Main
# pc path
path_in = "/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/rawdata/maestroP2I_231853_20240130_rebuilt.rsk"
path_out = "/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/"


# enter parameters of your local processing and somlit point
# must find a way to determine profile nb automatically
patm = 10.1325
latitude = 48.35
# note really a good idea to choose only one profile because it removes the upcast one


# calling processing function, we use the rsk object that have the same id as rsk_u and rsk_d processed files
raw,rsk,rsk_d,rsk_u, profile_nb = rsksproc.procRSK (path_in, patm, latitude, path_out)

#plotting
for param in ['salinity', 'temperature', 'chlorophyll-a']:
    
    
    rsksplt.plot_up_down(rsk_d, rsk_u, param, profile_nb)
    
       
    for cast in ['down','up']:
        if cast == 'down':
            fig1, axes1 = rsksplt.plot_raw_proc(rsk_d, rsk, param, cast, profile_nb)
        else:
            fig2, axes2 = rsksplt.plot_raw_proc(rsk_u, rsk, param, cast, profile_nb)


