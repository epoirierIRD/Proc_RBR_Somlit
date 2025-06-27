#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 12:44:55 2025

@author: epoirier
"""


import pyrsktools as pyrsk
import numpy as np
from datetime import datetime
import glob
import os
import RSKsomlit_proc as rsksproc
from collections import defaultdict
import re

# check if one single rsk_file has multiple dates or not 
# outputs a boolean and the list of the dates even if one date only
# works ok
def has_multiple_days_and_dates(rsk_file):
    with pyrsk.RSK(rsk_file) as rsk:
          
        rsk.readdata()  # Load the data
    
    if rsk.data is None or len(rsk.data) == 0:
        return False  # No data means no multiple days
    
    # Extract unique dates from the datetime column
    timestamps = rsk.data['timestamp']  # numpy.datetime64 array
   
    dates = np.array([ts.astype('datetime64[D]') for ts in timestamps])
    unique_dates = np.unique(dates)
    
    #unique_dates = {ts.date() for ts in rsk.data['timestamp']}
    
    return len(unique_dates) > 1, unique_dates

# function to scan the rsk files in my folder 
# split by date if I have a multiple rsk 
# output th list of files in my directory at the end
def scan_rsk(path_in):
    rsk_files = glob.glob(os.path.join(path_in, "*.rsk")) # creates the list of rsk files originals with path
    file_names = [os.path.basename(path) for path in rsk_files] # list of file names only
    print('Scanning RSK files, checking for multiple dates in files:')
    # Print each file name on a separate line
    for name in file_names:
        print(name)
    
    final_files = []
    final_dates = []
    
    for i, input_file in enumerate(rsk_files): # loop on my list of files
        is_multiple, dates = rsksproc.has_multiple_days_and_dates(input_file)
        # to create alist of final_dates
        print('found these dates in the files:',input_file)
        print(dates)
        
        # loop to create a list of dates, string format and avoid duplicates
        # Use a set for fast lookup
        seen = set(final_dates)
        for d in dates:
            d_str = str(d)  # ensure type matches (e.g., in case it's np.datetime64 or other)
            if d_str not in seen:
                final_dates.append(d_str)
                seen.add(d_str)
        
        if is_multiple: # when having multiple dates in one rsk
            print ('found multiple dates in file:') # print the file containing multiples
            print(input_file)
            # split the rsk if it is multiple, unique_days is a list of dates
            created_files = rsksproc.split_rsk_by_day(input_file) 
          
            print(f"✅ Created RSK files: {created_files}")
            final_files.extend(created_files) # add the created files in the list
        else: # when no muyliple date
        # we have to rename _YYYYmmdd when our file is not duplicate
        # this is for the routine find duplicate
            dt = np.datetime64(dates[0])
            date_str = str(dt).replace('-', '')
            rename_rsk_with_date(input_file, date_str)
            final_files.append(input_file) 
            
    final_files_names = [os.path.basename(path) for path in final_files]
    
    final_dates.sort(key=lambda d: datetime.strptime(d, "%Y-%m-%d")) # sort dates chronological
    
    print('Identified SOMLIT dates:')
    for date in final_dates:
        print(date)
    
    # remove duplicate files per day, some rsk files have the same day in it
    result = remove_duplicates(path_in)
    
    # sort files by date
    sorted_kept = sort_files_by_yymmdd(result['kept'])
    sorted_deleted = sort_files_by_yymmdd(result['deleted'])
    
    print('New list of RSK files (one per day) to process:')
    for f in sorted_kept:
        print(f" - {os.path.basename(f)}")
    print('Deleted files because duplicated')
    for f in sorted_deleted:
        print(f" - {os.path.basename(f)}")
        
def rename_rsk_with_date(file_path, date_str):
    """
    Rename an .rsk file by appending _YYYYMMDD before the extension.

    Parameters:
        file_path (str): Full path to the original .rsk file.
        date_str (str): Date string in format 'YYYYMMDD'.

    Returns:
        str: New full path after renaming.
    """
    if not file_path.endswith('.rsk'):
        raise ValueError("File must have a .rsk extension")

    dir_path = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    name_without_ext = os.path.splitext(base_name)[0]

    new_name = f"{name_without_ext}_{date_str}.rsk"
    new_path = os.path.join(dir_path, new_name)

    os.rename(file_path, new_path)
    print(f"✅ Renamed to: {new_name}")
    return new_path
        
# function to remove the duplicates for one date
# output the files deleted and the files kept
def remove_duplicates(path_in):
    pattern = "*.rsk"
    rsk_files = glob.glob(os.path.join(path_in, pattern))
    rsk_files = [f for f in rsk_files if os.path.isfile(f)]

    # Match filenames ending in _YYYYMMDD.rsk
    date_pattern = re.compile(r"_(\d{8})\.rsk$")

    files_by_date = defaultdict(list)

    for f in rsk_files:
        match = date_pattern.search(os.path.basename(f))
        if match:
            date_str = match.group(1)
            files_by_date[date_str].append(f)

    kept = []
    deleted = []

    for date_str, files in files_by_date.items():
        if len(files) == 1:
            kept.append(files[0])
            print(f"✅ Only one file for date {date_str}: {os.path.basename(files[0])}")
            continue

        # Sort by modification time, keep the most recent
        files.sort(key=os.path.getmtime, reverse=True)
        kept_file = files[0]
        to_delete = files[1:]

        kept.append(kept_file)
        print(f"⚠️ Multiple files for date {date_str}. Keeping:")
        print(f"   ➤ {os.path.basename(kept_file)}")

        for f in to_delete:
            try:
                os.remove(f)
                deleted.append(f)
                print(f"   🗑️ Deleted: {os.path.basename(f)}")
            except Exception as e:
                print(f"   ❗Error deleting {os.path.basename(f)}: {e}")

    return {"kept": kept, "deleted": deleted}

# function to sort the fils _YYYYMMDD chronologically
def sort_files_by_yymmdd(files):
    def extract_date(f):
        fname = os.path.basename(f)
        try:
            date_str = fname.split('_')[-1].replace('.rsk', '')
            return datetime.strptime(date_str, "%Y%m%d")
        except:
            return datetime.min  # fallback if pattern doesn't match

    return sorted(files, key=extract_date)




path_in="/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/summer_2024/temp"
    
scan_rsk(path_in)
              
                