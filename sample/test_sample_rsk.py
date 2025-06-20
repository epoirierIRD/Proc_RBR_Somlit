#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 11:05:36 2025

@author: epoirier1
"""

import pyrsktools as pyrsk
import matplotlib.pyplot as plt

with pyrsk.RSK("/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/rawdata/sample.rsk") as rsk:
    
    # Read data
    rsk.readdata()
    
    rsk.plotdata(channels=["pressure"], profile = 2, direction = "down", showcast=True)
    rsk.plotdata(channels=["pressure"], profile = 2, direction = "up", showcast=True)
    plt.show()
    
    rsk.computeprofiles()

    # Derived variables
    # Salinity
    rsk.deriveseapressure()
    rsk.derivedepth()
    rsk.derivevelocity()
    rsk.derivesalinity()
    rsk.derivesigma()
 
    #bin average on depth 0.25dbar or 25 cm
    #the binning processus is corrupting the showing of upcast
    
    
    rsk.binaverage(
       binBy = "depth",
       binSize = 1,
       boundary = [9,30.5], # 0.5 is the min pressure starting the binning and 10 the max
       direction = "up"
       )
    #rsk.readprocesseddata()
    
    param = ['conductivity',
          'temperature',
          # 'sea_pressure',
          'depth',
          'salinity',
          # 'speed_of_sound',
          # 'specific_conductivity',
          # 'dissolved_o2_saturation',
          # 'velocity',
          'density_anomaly'
          ]
    
    rsk.RSK2CSV(channels = 
        param, # list of parameters in argument
        profiles=3,
        comment= "upcast binned")
    

    '''    
    fig1, axes1 = rsk.plotprofiles(channels=["salinity"],profiles=range(1),direction="up")
    #rsk.binaverage(binSize = 5, boundary = 0.5, direction = "down")
    rsk.binaverage(
        binBy = "pressure",
        binSize = 10,
        boundary = [10,100], # 0.5 is the min pressure starting the binning and 10 the max
        direction = "up"
        )
    fig2, axes2 = rsk.plotprofiles(channels=["salinity"],profiles=range(1),direction="up")

    fig, axes = rsk.mergeplots(
                [fig1,axes1],
                [fig2,axes2],
                )
    for ax in axes:
        line = ax.get_lines()[-1]
        plt.setp(line, linewidth=0.5, marker = "o", markerfacecolor = "w")
        plt.legend(labels=["Original data","Processed data"])
    
     '''
        
    
    # rsk.binaverage(
    #     binBy = "pressure",
    #     binSize = 1,
    #     boundary = [5,300], # 0.5 is the min pressure starting the binning and 10 the max
    #     direction = "up"
    #     )
    
    
'''
    
    # Plot a few profiles of temperature, conductivity, and chlorophyll
    fig, axes = rsk.plotprofiles(
        channels=["temperature"],
        profiles=2,
        direction="both",
        reference='pressure'
        )
    
'''
plt.show()
