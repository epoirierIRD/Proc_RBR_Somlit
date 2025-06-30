# WORK IN PROGRESS
# Proc_RBR_Somlit
Processing of RBR ctd cast for Somlit coastal observatory in Plouzane, France.
The goal is to create a 'routine' for the RBR maestro data to process the raw binary rsk file
and save it to a csv file format as per the SOMLIT DB.
The idea is to help Emilie having less operations to do manually. SBE processing asks her a few copy/paste before having 
the proper csv format for somlit.

The goal is also to show that RBR data are as valuable as SBE ones. Apply also the same kind of processing as for the SBE to
have a continuous time serie even swaping from sbe to rbr.

Off course RBR is not SBE and processing will not be the same but results on this intercomparison day 20240130
 must show as little difference as possible and csv output file must be just like the SBE ones to be absorbed in the somlit databases.

Emilie did the processing of SBE data
The goal is to do a processing of the profile of the RBR maestro using RSKtools library in python to produce
a profile similar as the SBE one and then compare them.


The main reference found on the web for processing RBR CTD data is Halverson et al. 2017.

We also test a RBR routine on other rsk files as per the folders visible in this repo.

30/06/2025, updated main_summer_2024.py and checked that works fine. Next improvment to input the somlit number in a the folder name and perhaps on the graphs


