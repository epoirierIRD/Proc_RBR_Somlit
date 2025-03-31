#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 12:07:45 2025

@author: epoirier1
"""


import pyrsktools as pyrsk
import numpy as np
import matplotlib.pyplot as plt

# with pyrsk.RSK("/home/epoirier1/Documents/PROJETS/2025/Proc_RBR_Somlit/rawdata/maestroP2I_231853_20240130_rebuilt.rsk") as rsk:
    
#     rsk.readdata()
#     # print(rsk)
#     # rsk.computeprofiles(1,5)
#     # print(rsk)
#     # rsk.regions


#     profiles = rsk.getprofilesindices(range(0, 3), direction="both")
#     for profileIndices in profiles:
#         print(rsk.data[profileIndices])
#     fig, axes = rsk.plotprofiles(
#         channels=["conductivity", "temperature", "salinity"],

# profiles = profiles,

#        direction="down",

#    )

# plt.show()

with pyrsk.RSK("/home/epoirier1/Documents/PROJETS/2025/Proc_RBR_Somlit/rawdata/maestroP2I_231853_20240130_rebuilt.rsk") as rsk:

   rsk.readdata()

   rsk.deriveseapressure()

   rsk.derivesalinity()


   fig, axes = rsk.plotprofiles(

       channels=["conductivity", "temperature", "salinity"],

       profiles=range(0, 3),

       direction="down",

   )

   plt.show()
