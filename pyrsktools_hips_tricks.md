
Advanced processing below for SOMLIT CTD profile point in Ste Anne du Porzic

Hips and tricks with pyrsktools commands
# REGIONS
Do rsk.regions to have a list of RegionCast and RegionProfile
the regionID values are unclear
rsk.regions envoie un tuple on fait rsk.regions[1] pour appeler la première valeur
et rsk.regions[1].regionID pour avoir le regionID de ce CAST
rsk.regions[1] to call region 1
1 profile c'est deux cast, on voit bien cela dans profile.regions
in profile we have the beginning of downcast and the end of up cast in terms of time

# CHANNELS
rsk.printchannels to view the metadat info of the probe
rsk.channels to get the channels recorded, use the longName in the rsk.plotdata('LongName')

# DATA
rsk.data is a numpy array with all the values + channels names
print(rsk) gives the status of the rsk file, ex nb of regions populated
rsk.data[39] reads the full line for recording n°39, 39 is the indice

PLOT
rsk.plotdata, plt.show() to plot as timeseries
