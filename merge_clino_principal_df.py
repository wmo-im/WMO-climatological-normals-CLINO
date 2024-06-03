## Importations
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 
import datetime as dt
import imageio
import requests
import sharepy
import math
from tqdm import tqdm

"""
Create a function that merge the 8 principal clino data frames:

 - wmo_normals_9120_DP01
 - wmo_normals_9120_MNVP
 - wmo_normals_9120_MSLP
 - wmo_normals_9120_PRCP
 - wmo_normals_9120_TAVG
 - wmo_normals_9120_TMAX
 - wmo_normals_9120_TMIN
 - wmo_normals_9120_TSUN

create a merged solution with :
- 1 feature per month (12 in total)
- 1 row per mesure : n rows *8 

"""


def merge_clino_principal_df():

    ## Creating list of additional information  
    list_month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Annual"]

    list_unit = ["Days", "hPa", "hPa", "mm", "Deg_C", "Deg_C", "Deg_C", "hours"]

    list_suffixes = ["Total days with ≥1 mm precipitation", "Mean Vapor Pressure", "Mean Sea Level Pressure", "Precipitation", "Mean Temperature", "Mean Maximum Temperature", "Mean Minimum Temperature", "Total Sunshine"]

    list_files = ["wmo_normals_9120_DP01", "wmo_normals_9120_MNVP", "wmo_normals_9120_MSLP", "wmo_normals_9120_PRCP", "wmo_normals_9120_TAVG", "wmo_normals_9120_TMAX", "wmo_normals_9120_TMIN", "wmo_normals_9120_TSUN"]

    list_clino = []
    
    ## Upload the data and clean the string
    for file in list_files:
        df_clino = pd.read_csv("data/data-composite-primary-parameters/" + file + ".csv")
        df_clino.columns = df_clino.columns.str.strip()
        df_clino['Station'] = df_clino['Station'].str.strip()
        list_clino.append(df_clino)



    # Create a measure type column 
    for i, df in enumerate(list_clino):
        df["mesure"] = [list_suffixes[i] for a in range(len(df))]
        df["unit"] = [list_unit[i] for a in range(len(df))]
    
    # Concatenate the 8 dataframes
    df_clino_conc = pd.concat(list_clino)
    
    
    pd.to_numeric(df_clino_melted["value"])
    
    ## cleaning 
    for month in list_month:
        print("-99.9 values remaining: ")
        print("Value count : " + str(df_clino_conc[month].value_counts()))
        print("Before : " + str(df_clino_conc.loc[df_clino_conc[month]==-99.90][month].count()))
        df_clino_conc.loc[df_clino_conc[month]==-99.90] = None
        df_clino_conc.loc[df_clino_conc[month]<-99] = None
        print("After : " + str(df_clino_conc.loc[df_clino_conc[month]==-99.90][month].count()))
        print("Value count : " + str(df_clino_conc[month].value_counts()))
    print("result : " + str(df_clino_conc.loc[df_clino_conc[month]==-99.9][month].count()))
    
    ## download the csv
    df_clino_conc.to_csv('data/Clino_concat.csv', index=False)
    
    
    ## print information about clino
    for i, df_clino in enumerate(list_clino):
        print("Result for " + str(list_suffixes[i]))
        print(["Unique WIGOS_ID : " + str(df_clino['WIGOS_ID'].nunique()),
               "Unique ID : " + str(df_clino['ID'].nunique()), 
               "Unique station : " + str(df_clino['Station'].nunique()), 
               "Size : " + str(len(df_clino)), 
               "Empty ID : " + str(df_clino['ID'].isnull().sum()),
               "Empty WIGOS_ID : " + str(df_clino['WIGOS_ID'].isnull().sum()),
               "Empty station : " + str(df_clino['Station'].isnull().sum())])
        print("\n")

    
# Execute the function
merge_clino_principal_df()