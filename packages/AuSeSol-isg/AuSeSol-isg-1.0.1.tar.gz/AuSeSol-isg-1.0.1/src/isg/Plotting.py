
import pandas as pd 
import numpy as np
from datetime import datetime
import dask.dataframe as dd
import dask
import os 
import glob 
import snowflake.connector as connector
import seaborn as sns
import matplotlib.pyplot as plt 



########################################################################

def highlight_missing_data(dataframe, signal, freq)-> "None":
    
    '''
    Plot sensor signal with highlighed missing (nan values) data in red. The index of the dataframe has to be of type datetime. 
    
    parameters:
    -----------
    dataframe: pd.Dataframe
        The dataframe that contains the signal 
        
    signal: str
        Signal name which need to be plotted
        
    freq: str
        The frequency of the provided signal. 
        example: "1S", "5S" "T" 
    
    '''
    max_signal = 1.02 * dataframe.loc[:, signal].max() # value for max visual threshhold 
    
    df_with_nan_values = dataframe.asfreq(freq) # extract dataframe with nan values included
    
    df_imputed = df_with_nan_values.fillna(value= max_signal) # impute the nan values with the max signal value
    
    # plotting to overlaping figures
    
    
    fig = plt.figure(figsize=(20,5))
    sns.set()
    
    # first figure 
    ax = df_with_nan_values[signal].plot()
    
    # second figure
    plt.fill_between(x=df_imputed.index,
                     y1=0,
                     y2= max_signal,
                     where = df_imputed[signal] == max_signal, color="r" , alpha=0.4)



    
######################################################################################