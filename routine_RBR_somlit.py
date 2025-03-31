#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 10:58:39 2025

@author: epoirier1

Based on matlab script example from Halverson et al. 2017
"""
import pyrsktools as pyrsk
import numpy as np
import matplotlib.pyplot as plt
'''

# basic plot below

with pyrsk.RSK("/home/epoirier1/Documents/PROJETS/2025/Proc_RBR_Somlit/rawdata/sample.rsk") as rsk:
    # Print a list of all the channels in the RSK file
    rsk.printchannels()
    # Read data
    rsk.readdata()
    # Derive sea pressure from total pressure
    rsk.deriveseapressure()
    # Plot a few profiles of temperature, conductivity, and chlorophyll
    fig, axes = rsk.plotprofiles(
        channels=["conductivity", "temperature"],
        profiles=range(0, 3),
        direction="down",
    )
    plt.show()
'''

# Advanced processing below for SOMLIT point in Ste Anne du Porzic

# Hips and tricks with pyrsktools commands

# Do rsk.regions to have a list of RegionCast and RegionProfile
# rsk.printchannels to view the metadat info of the probe
# rsk.channels to get the channels recorded, use the longName in the rsk.plotdata('LongName')
# rsk.data is a numpy array with all the values + channels names
# rsk.plotdata, plt.show() to plot as timeseries


# using the method below is the right way to read the data
# with pyrsk.RSK("/home/epoirier1/Documents/PROJETS/2025/Proc_RBR_Somlit/rawdata/sample.rsk") as rsk:
    
with pyrsk.RSK("/home/epoirier1/Documents/PROJETS/2025/Proc_RBR_Somlit/rawdata/maestroP2I_231853_20240130_rebuilt.rsk") as rsk:
   
    # read the data first
    rsk.readdata()
   
    
    # Use atmopsheric pressure patm to calculate sea pressure
    # Enter sea pressure of the somlit day here
    # In an ideal way the barometric pressure must be measured at each somlit and entered here
    # remind: -1hPa (air pressure) = +1cm sealevel
    # -100hPa = -1dbar = +1m sealevel
    patm = 10.1325
    rsk.deriveseapressure(patm)
    
    # Keep a copy of the raw data to compare with the processed ones
    raw = rsk.copy()
    
    # Correct for A2D (analog to digital) zero-holder, find the missing samples and interpolate
    rsk.correcthold(action = "interp")
    
    # Low-pass filtering, windowlength is the number of values to use to calculate an average
    # We run at 2Hz, it is slower than the RBR (4Hz) so we won't apply any filter
    
    # rsk.smooth(channels = ["temperature"], windowLength = 5)
    
    # realignement CT
    # time lag of the temperature sensor
    # regarding the profiling speed very slow at somlit, and the red family of conductimeter
    # this lag must be slow << 10 ms (from processing specs, pyrsktools)
    # choosen arbitrary 5 ms shift of the temperature data earlier
    # lag = -0.005
    
    #there is an issue here
    
    rsk.alignchannel("temperature", 0)
    
    # removing loops due to swell and probe measuring its wake
    # this might important in shallow coastal waters just as somlit location
      
    # first derivedepth to calculate depth from corrected sea pressure
    # latitude of somlit point at Plouzané written below
    rsk.derivedepth(latitude=48.35, seawaterLibrary="TEOS-10")
    
    # derive velocity , calculate velocity from depth and time
    # possible to add an argument here to do a window average of the salinity
    # not needed here as we go slow
    rsk.derivevelocity()
    
    # then remove loops
    # speed treshold 0.1m/s mini profiling speed to consider
    # this values is important as all the data below this speed value are removed
    rsk.removeloops(direction= "down", threshold= 0.05)
    
    # Derived variables
    # Salinity
    rsk.deriveseapressure()
    rsk.derivedepth()
    rsk.derivevelocity()

    rsk.derivesalinity()
    rsk.derivesigma()

    # Print a list of channels in the rsk file
    rsk.printchannels()
    
    # #bin average on depth 0.25dbar or 25 cm
    # rsk.binaverage(
    # binBy = "sea_pressure",
    # binSize = 0.25,
    # boundary = [0.5, 5.5],
    # direction = "up"
    # )
    

    
fig1, axes1 = rsk.plotprofiles(channels=["salinity"],profiles=range(1),direction="down")
rsk.binaverage(binSize = 0.25, boundary = 0.5, direction = "down")
fig2, axes2 = rsk.plotprofiles(channels=["salinity"],profiles=range(1),direction="down")

fig, axes = rsk.mergeplots(
         [fig1,axes1],
         [fig2,axes2],
     )
for ax in axes:
    line = ax.get_lines()[-1]
    plt.setp(line, linewidth=0.5, marker = "o", markerfacecolor = "w")
plt.legend(labels=["Original data","Processed data"])
plt.show()

rsk.RSK2CSV(channels = ["temperature","par","conductivity","dissolved_o2_concentration","salinity","depth"], profiles= range(0,3), comment= "for Emilie")
    
    
'''    
# bout de code pour visualiser un seul profil et 3 variables
with pyrsk.RSK("/home/epoirier1/Documents/PROJETS/2025/Proc_RBR_Somlit/rawdata/maestroP2I_231853_20240130.rsk") as rsk:
    rsk.readdata()
    rsk.deriveseapressure()
    rsk.derivesalinity()
    fig, axes = rsk.plotprofiles(

       channels=["conductivity", "temperature", "salinity"],

       profiles=range(0, 1),

       direction="down",

   )
   

plt.show()
'''