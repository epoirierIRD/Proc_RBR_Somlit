#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 13:47:16 2025

@author: epoirier
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import os


# function to read the CSV Somlit type file from my programs
# not used because missing channels in the final somlit file compared with what
# we want to compare in the SBE data (more channels)
def parse_somlit_file(filepath):
    """
    Parses a SOMLIT-like CSV file with header and metadata.

    Args:
        filepath (str): Path to the input file.

    Returns:
        pd.DataFrame: Cleaned data as DataFrame.
    """

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find the line that starts with 'ID_SITE' – it's the header
    for i, line in enumerate(lines):
        if line.strip().startswith("ID_SITE"):
            header_idx = i
            break
    else:
        raise ValueError("No header line starting with 'ID_SITE' found.")

    # Now use pandas to read from that line onward
    df = pd.read_csv(
        filepath,
        sep=";",
        skiprows=header_idx, # skip line with variable too
        encoding="utf-8"
    )

    # Drop completely empty rows (e.g. lines of just semicolons)
    df.dropna(how="all", inplace=True)
    
    # Remove first row having the units
    df = df.iloc[1:].reset_index(drop=True)

    # Combine date + time into datetime
    df["DATETIME"] = pd.to_datetime(df["DATE"] + " " + df["HEURE"])
    # Convert to datetime64 format
    df['DATETIME'] = pd.to_datetime(df['DATETIME'])
    

    # Optional: reorder or drop columns
    df = df[["DATETIME", "ID_SITE", "TEMPERATURE", "FLUORESCENCE", "PAR", "SALINITE", "PROFONDEUR"]]
    
    # assign DATETIME colmun as index
    df.set_index('DATETIME', inplace=True)

    return df





# ********************************************************************************
# Function to read a csv file outputted from procRSK custom function
# It stores the data in a dataframe
def read_RBR_csv (file_path):
    # args: - file_path: str csv file coming from proCRSK function, either down or up cast
    
    
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    # Step 2: Find the last line starting with '//'
    header_line_idx = None
    for idx, line in enumerate(lines):
        if line.startswith("//"):
            header_line_idx = idx
    
    # Step 3: Read the file into DataFrame, skipping earlier lines
    # Beware of sep ',   ' 4 spaces after comma
    df = pd.read_csv(
        file_path,
        sep =',    ',
        skiprows=header_line_idx + 1,     # Skip all lines before actual data
        header=None ,                      # No header in data part
        engine = "python"
    )
    
    # Step 4: Set the header from the last '//' line
    column_names = lines[header_line_idx].lstrip("//").strip().split(",    ")
    df.columns = column_names
    
    # remove line with nan
    df=df.dropna()
    
    # Convert the first column to datetime using your format
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='%Y-%m-%dT%H:%M:%S.%f')
    
    # Set the first column as the index, and avoid warning caused
    # by aving diffrent object types in the index: str, numerical, etc...
    df[df.columns[0]] = df[df.columns[0]].infer_objects()
    df.set_index(df.columns[0], inplace=True)  
    
    data = pd.Series([1, '2', 3])  # mixed types
    index = pd.Index(data.infer_objects())  # ensures inference like before
    
    return df




# function to read csv file from sbe created via export from xlsx
def parse_custom_sbe(filepath):
    # Read file, skip second line (units), first line is header
    df = pd.read_csv(
        filepath,
        sep=';',
        skiprows=[1],  # skip the units row
        decimal=',',    # interpret comma as decimal separator
        dayfirst=True,  # because date format is DD/MM/YYYY
    )

    # Combine date and time into a datetime column
    df['DATETIME'] = pd.to_datetime(df['DD MMM YYYY'] + ' ' + df['HH:MM:SS'], dayfirst=True)

    # Set DATETIME as index
    df.set_index('DATETIME', inplace=True)

    # Optional: drop original date/time columns if you want
    df.drop(columns=['DD MMM YYYY', 'HH:MM:SS'], inplace=True)

    return df

# rename the columns of sbe df with the ones from rbr df using position id
# + apply a factor to convert DO from ml/L (sbe) to micromol/L (RBR)
def rename_sbe_columns(df_sbe, df_rbr):
    
    # apply a factor to DO values from SBE to convert units
    # from ml/L to micromol/L
    df_sbe['Oxygène'] = df_sbe['Oxygène'] * 44.66
    
    # rename columns as per the RBR names
    df_sbe = df_sbe.rename(columns={
    'temp': df_rbr.columns[1],
    'FLUO': df_rbr.columns[6],
    'Par': df_rbr.columns[4],
    'conductivité':  df_rbr.columns[0],
    'Oxygène': df_rbr.columns[3],
    'turbidité': df_rbr.columns[8],
    'Sal00': df_rbr.columns[10],
    'profondeur': df_rbr.columns[9],
    'densité': df_rbr.columns[11]
    })
    
    return df_sbe



# works for upcast or downcast
# prefer the next function to plot everything on the same graph
def plot_and_save_comparisons_all_columns(df_sbe, df_rbr, depth_col='depth(m)', save_folder='figures'):
    """
    Compare all common numeric columns from SBE and RBR:
    - Plot each parameter vs depth
    - Plot the difference (SBE - RBR) vs depth (only at common depths)
    - Save plots as PNG files

    Args:
        df_sbe (pd.DataFrame): SBE dataset
        df_rbr (pd.DataFrame): RBR dataset
        depth_col (str): Name of the depth column
        save_folder (str): Output directory
    """
    os.makedirs(save_folder, exist_ok=True)

    # Ensure depth columns are numeric and rounded to avoid tiny float mismatches
    df_sbe[depth_col] = pd.to_numeric(df_sbe[depth_col], errors='coerce').round(4)
    df_rbr[depth_col] = pd.to_numeric(df_rbr[depth_col], errors='coerce').round(4)

    # Find common depths
    common_depths = np.intersect1d(df_sbe[depth_col].dropna().unique(), df_rbr[depth_col].dropna().unique())

    if len(common_depths) == 0:
        print("❌ No common depth values found between datasets.")
        return

    # Filter both DataFrames to common depths
    df_sbe_common = df_sbe[df_sbe[depth_col].isin(common_depths)].copy()
    df_rbr_common = df_rbr[df_rbr[depth_col].isin(common_depths)].copy()

    # Sort by depth for plotting
    df_sbe_common = df_sbe_common.sort_values(depth_col)
    df_rbr_common = df_rbr_common.sort_values(depth_col)

    # Get common numeric columns (excluding depth)
    common_cols = [
        col for col in df_rbr.columns
        if col in df_sbe.columns
        and col != depth_col
        and np.issubdtype(df_rbr[col].dtype, np.number)
    ]

    if not common_cols:
        print("❌ No common numeric columns to compare.")
        return

    for param in common_cols:
        print(f"📈 Processing '{param}'...")

        # Merge on depth to align values exactly
        merged = pd.merge(
            df_sbe_common[[depth_col, param]],
            df_rbr_common[[depth_col, param]],
            on=depth_col,
            suffixes=('_sbe', '_rbr')
        )

        if merged.empty:
            print(f"⚠️ No matching depth values with data for '{param}'. Skipping.")
            continue

        # Plot parameter vs depth
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(merged[f"{param}_sbe"], merged[depth_col], label='SBE', marker='o')
        ax.plot(merged[f"{param}_rbr"], merged[depth_col], label='RBR', marker='x')
        ax.invert_yaxis()
        ax.set_xlabel(f"{param} (units)")
        ax.set_ylabel("Depth (m)")
        ax.set_title(f"{param} Profile: SBE vs RBR")
        ax.legend()
        ax.grid(True)
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
        plt.tight_layout()

        safe_param = ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in param)
        fig_path_raw = os.path.join(save_folder, f"{safe_param}_profile.png")
        fig.savefig(fig_path_raw, dpi=150)
        plt.close(fig)

        # Compute difference on common depths
        diff = merged[f"{param}_rbr"] - merged[f"{param}_sbe"]

        # Plot difference
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(diff, merged[depth_col], label='RBR - SBE', color='red', marker='.')
        ax.invert_yaxis()
        ax.set_xlabel(f"{param} Difference")
        ax.set_ylabel("Depth (m)")
        ax.set_title(f"{param} Difference (RBR - SBE)")
        ax.grid(True)
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
        plt.tight_layout()

        fig_path_diff = os.path.join(save_folder, f"{safe_param}_difference.png")
        fig.savefig(fig_path_diff, dpi=150)
        plt.close(fig)

        print(f"✅ Saved: {fig_path_raw} and {fig_path_diff}")


# produces figures with up and down cast and both sbe and rbr data on the same graphe, great
def plot_comparisons_up_down(
    df_sbe_down, df_rbr_down,
    df_sbe_up, df_rbr_up,
    depth_col='depth(m)',
    save_folder='figures'
):
    os.makedirs(save_folder, exist_ok=True)

    def preprocess(df):
        df = df.copy()
        df[depth_col] = pd.to_numeric(df[depth_col], errors='coerce').round(4)
        return df.dropna(subset=[depth_col])

    df_sbe_down = preprocess(df_sbe_down)
    df_rbr_down = preprocess(df_rbr_down)
    df_sbe_up = preprocess(df_sbe_up)
    df_rbr_up = preprocess(df_rbr_up)

    # Get common numeric columns
    common_cols = [
        col for col in df_rbr_down.columns
        if col in df_sbe_down.columns
        and col != depth_col
        and np.issubdtype(df_rbr_down[col].dtype, np.number)
    ]

    if not common_cols:
        print("❌ No common numeric columns to compare.")
        return

    for param in common_cols:
        print(f"📈 Processing '{param}'...")

        # Prepare merged data for both casts
        def merge_on_depth(df1, df2):
            common_depths = np.intersect1d(df1[depth_col].unique(), df2[depth_col].unique())
            df1_common = df1[df1[depth_col].isin(common_depths)]
            df2_common = df2[df2[depth_col].isin(common_depths)]
            return pd.merge(
                df1_common[[depth_col, param]],
                df2_common[[depth_col, param]],
                on=depth_col,
                suffixes=('_sbe', '_rbr')
            ).sort_values(depth_col)

        merged_down = merge_on_depth(df_sbe_down, df_rbr_down)
        merged_up = merge_on_depth(df_sbe_up, df_rbr_up)

        # Profile Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        if not merged_down.empty:
            ax.plot(merged_down[f"{param}_sbe"], merged_down[depth_col], 'o-', label='SBE Downcast')
            ax.plot(merged_down[f"{param}_rbr"], merged_down[depth_col], 'x-', label='RBR Downcast')
        if not merged_up.empty:
            ax.plot(merged_up[f"{param}_sbe"], merged_up[depth_col], 'o--', label='SBE Upcast', alpha=0.6)
            ax.plot(merged_up[f"{param}_rbr"], merged_up[depth_col], 'x--', label='RBR Upcast', alpha=0.6)

        ax.invert_yaxis()
        ax.set_xlabel(f"{param} (units)")
        ax.set_ylabel("Depth (m)")
        ax.set_title(f"{param} Profile: Upcast & Downcast (SBE vs RBR)")
        ax.legend()
        ax.grid(True)
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
        plt.tight_layout()

        safe_param = ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in param)
        fig_path_profile = os.path.join(save_folder, f"{safe_param}_profile.png")
        fig.savefig(fig_path_profile, dpi=150)
        plt.close(fig)

        # Difference Plot (RBR - SBE)
        fig, ax = plt.subplots(figsize=(6, 6))
        if not merged_down.empty:
            diff_down = merged_down[f"{param}_rbr"] - merged_down[f"{param}_sbe"]
            ax.plot(diff_down, merged_down[depth_col], 'r-', label='Downcast (RBR - SBE)', marker='.')
        if not merged_up.empty:
            diff_up = merged_up[f"{param}_rbr"] - merged_up[f"{param}_sbe"]
            ax.plot(diff_up, merged_up[depth_col], 'b--', label='Upcast (RBR - SBE)', marker='.')

        ax.invert_yaxis()
        ax.set_xlabel(f"{param} Difference")
        ax.set_ylabel("Depth (m)")
        ax.set_title(f"{param} Difference (RBR - SBE)")
        ax.grid(True)
        ax.legend()
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
        plt.tight_layout()

        fig_path_diff = os.path.join(save_folder, f"{safe_param}_difference.png")
        fig.savefig(fig_path_diff, dpi=150)
        plt.close(fig)

        print(f"✅ Saved: {fig_path_profile} and {fig_path_diff}")



def plot_comparisons_up_down_rbr1853_6135(
    df_rbr1853_down, df_rbr6135_down,
    df_rbr1853_up, df_rbr6135_up,
    depth_col='depth(m)',
    save_folder='figures'
):
    os.makedirs(save_folder, exist_ok=True)

    def preprocess(df):
        df = df.copy()
        df[depth_col] = pd.to_numeric(df[depth_col], errors='coerce').round(4)
        return df.dropna(subset=[depth_col])

    df_rbr1853_down = preprocess(df_rbr1853_down)
    df_rbr6135_down = preprocess(df_rbr6135_down)
    df_rbr1853_up = preprocess(df_rbr1853_up)
    df_rbr6135_up = preprocess(df_rbr6135_up)

    # Get common numeric columns
    common_cols = [
        col for col in df_rbr6135_down.columns
        if col in df_rbr1853_down.columns
        and col != depth_col
        and np.issubdtype(df_rbr6135_down[col].dtype, np.number)
    ]

    if not common_cols:
        print("❌ No common numeric columns to compare.")
        return

    for param in common_cols:
        print(f"📈 Processing '{param}'...")

        # Merge on common depths
        def merge_on_depth(df1, df2):
            common_depths = np.intersect1d(df1[depth_col].unique(), df2[depth_col].unique())
            df1_common = df1[df1[depth_col].isin(common_depths)]
            df2_common = df2[df2[depth_col].isin(common_depths)]
            return pd.merge(
                df1_common[[depth_col, param]],
                df2_common[[depth_col, param]],
                on=depth_col,
                suffixes=('_1853', '_6135')
            ).sort_values(depth_col)

        merged_down = merge_on_depth(df_rbr1853_down, df_rbr6135_down)
        merged_up = merge_on_depth(df_rbr1853_up, df_rbr6135_up)

        # Profile Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        if not merged_down.empty:
            ax.plot(merged_down[f"{param}_1853"], merged_down[depth_col], 'o-', label='RBR1853 Downcast')
            ax.plot(merged_down[f"{param}_6135"], merged_down[depth_col], 'x-', label='RBR6135 Downcast')
        if not merged_up.empty:
            ax.plot(merged_up[f"{param}_1853"], merged_up[depth_col], 'o--', label='RBR1853 Upcast', alpha=0.6)
            ax.plot(merged_up[f"{param}_6135"], merged_up[depth_col], 'x--', label='RBR6135 Upcast', alpha=0.6)

        ax.invert_yaxis()
        ax.set_xlabel(f"{param} (units)")
        ax.set_ylabel("Depth (m)")
        ax.set_title(f"{param} Profile: RBR1853 vs RBR6135 (Upcast & Downcast)")
        ax.legend()
        ax.grid(True)
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
        plt.tight_layout()

        safe_param = ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in param)
        fig_path_profile = os.path.join(save_folder, f"{safe_param}_profile.png")
        fig.savefig(fig_path_profile, dpi=150)
        plt.close(fig)

        # Difference Plot (RBR6135 - RBR1853)
        fig, ax = plt.subplots(figsize=(6, 6))
        if not merged_down.empty:
            diff_down = merged_down[f"{param}_6135"] - merged_down[f"{param}_1853"]
            ax.plot(diff_down, merged_down[depth_col], 'r-', label='Downcast (6135 - 1853)', marker='.')
        if not merged_up.empty:
            diff_up = merged_up[f"{param}_6135"] - merged_up[f"{param}_1853"]
            ax.plot(diff_up, merged_up[depth_col], 'b--', label='Upcast (6135 - 1853)', marker='.')

        ax.invert_yaxis()
        ax.set_xlabel(f"{param} Difference")
        ax.set_ylabel("Depth (m)")
        ax.set_title(f"{param} Difference (RBR6135 - RBR1853)")
        ax.grid(True)
        ax.legend()
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
        plt.tight_layout()

        fig_path_diff = os.path.join(save_folder, f"{safe_param}_difference.png")
        fig.savefig(fig_path_diff, dpi=150)
        plt.close(fig)

        print(f"✅ Saved: {fig_path_profile} and {fig_path_diff}")



'''
# downcast
df_rbr_2 = read_RBR_csv('/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240130/procdata/maestroP2I_231853_20240130_rebuilt/downcast/maestroP2I_231853_20240130_rebuilt_profile0.csv')
df_sbe = parse_custom_sbe('/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240130/proc_data/SBE19plusV2cast36testRBR300124_down.csv')
df_sbe = rename_sbe_columns(df_sbe, df_rbr_2)
plot_and_save_comparisons_all_columns(df_sbe, df_rbr_2)


# upcast
df_rbr_2 = read_RBR_csv('/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240130/procdata/maestroP2I_231853_20240130_rebuilt/upcast/maestroP2I_231853_20240130_rebuilt_profile0.csv')
df_sbe = parse_custom_sbe('/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240130/proc_data/SBE19plusV2cast36testRBR300124_up.csv')
df_sbe = rename_sbe_columns(df_sbe, df_rbr_2)
plot_and_save_comparisons_all_columns(df_sbe, df_rbr_2)

'''
# upcast and downcast together
# Great that works

df_rbr_1853_up = read_RBR_csv('/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240912/procdata/231853_20240912_1229/upcast/231853_20240912_1229_profile0.csv')
df_rbr_6135_up = read_RBR_csv('/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240912/procdata/236135_20240912_1238/upcast/236135_20240912_1238_profile0.csv')


df_rbr_1853_down = read_RBR_csv('/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240912/procdata/231853_20240912_1229/downcast/231853_20240912_1229_profile0.csv')
df_rbr_6135_down = read_RBR_csv('/home/epoirier/Documents/PROJETS/2025/Proc_RBR_Somlit/20240912/procdata/236135_20240912_1238/downcast/236135_20240912_1238_profile0.csv')

plot_comparisons_up_down_rbr1853_6135(df_rbr_1853_down, df_rbr_6135_down, df_rbr_1853_up, df_rbr_6135_up)








