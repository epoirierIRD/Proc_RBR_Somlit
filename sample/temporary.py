#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 12:07:45 2025

@author: epoirier1
"""


import pyrsktools as pyrsk
import numpy as np
import matplotlib.pyplot as plt

with pyrsk.RSK("/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/rawdata/maestroP2I_231853_20240130_rebuilt.rsk") as rsk:
    
    
    '''
    # beacuse changement
    # de hardware constaté sur la RBRm donc la maestro depuis 2023
    # routine inspirée de X. Capet faite sous matlab
    
    
    # because problème d'attribution des canaux 8,9,10 en choloro fdom et turbidity avecle nouveau capteur tridente
    
    print(rsk.instrument.model)
    
    
    
    # bout de code matlab de xavier
    if rsk1.instruments.model =='RBRmaestro3'
        II=min(find(~isnan(rsk1.data(1).tstamp(:))));
dateRBRm=datevec(rsk1.data(1).tstamp(II));yearRBRm=dateRBRm(1);
        if yearRBRm<2023
itemp=2;ifluo=4;icdom=5;iturb=6;itempo2=7;io2=8;ipar=9;ipres=10;idepth=11;isalt=12;
          strgTemp='Temperature1'; RFUB=42.7;
        else
itemp=2;ifluo=8;icdom=9;iturb=7;itempo2=4;io2=5;ipar=6;ipres=10;idepth=11;isalt=12;
          strgTemp='Temperature1';RFUB=1;new_rbrm=1;
        end 
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    rsk.readdata()
    print(rsk)
    rsk.computeprofiles(1,5)
    print(rsk)
    print(rsk.regions)
    #declare variable
    myprofile = 0;
    # we iterate on the full rsk.regions tuple and 
    # find the tuple position of my profile of interest
    for i in range(len(rsk.regions)):
        if rsk.regions[i].label == 'Profile 0':
            myprofile = i
    print(myprofile+1)
    

    '''
    profiles = rsk.getprofilesindices(range(0, 3), direction="both")
    for profileIndices in profiles:
        print(rsk.data[profileIndices])
        
    fig, axes = rsk.plotprofiles(
        channels=["conductivity", "temperature", "salinity"],

    profiles = profiles,

        direction="down",
        
    )

plt.show()

'''


'''
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
'''