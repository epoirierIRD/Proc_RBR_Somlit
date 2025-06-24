#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 16:40:02 2025

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


rsksproc.split_rsk_by_date(
    input_rsk_path ='/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/summer_2024/temp/231853_20240806_1338 somlit25à29.rsk' ,
    output_folder='/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/summer_2024')