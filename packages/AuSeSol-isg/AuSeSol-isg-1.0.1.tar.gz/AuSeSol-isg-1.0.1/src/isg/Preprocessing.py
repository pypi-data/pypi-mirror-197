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

#########################################



def read_data_from_parquet(parquet_path,
                           feature_list=None,
                           filter_features=None,
                          **kwargs
                          ) -> "dask.dataframe":
    '''
    
    Read a paruqet into a panda dataframe
    
    
    Parameters:
    -----------
    parquet_path: str
        Defines the path to the parquet (including the name) relativ to the skript. The functuion also automatically sets
        the index as parsed datetime timestamp. 
    
    feature_list: list of String, defult= None
        A list of features (columns) that are required from the dataframe. Make sure the feature (column) names match.
        
    apply_filter: in form of (column_name_str, argument, value ), defult= None
        Applies filter to one of more columns. 
        argument_exp: "<" , "==", ">"
        example: ("Datetime","<", "2020-02")

   '''
    
    
    dataframe = dd.read_parquet(parquet_path, columns=feature_list, index="Datetime",filters= filter_features).compute()      
    
    dataframe.index = pd.to_datetime(dataframe.index) 
    
    return dataframe


####################################################


def change_parquet_names_to_date(parquets_directory_path) -> None :

    '''
    
    Change the names of parquet files in a dirctory to name of the date 
    
    Parameters:
    -----------
    parquets_directory_path: str
        Defines the path to the parquet (including the name) relativ to the skript. 
    
    Example:
        part.10.parquet --> 02-03-2021.parquet
   '''
    
    
    # define all parquet files in the directory
    parquet_files = glob.glob(parquets_directory_path + "/part*") 
    
    # initialize a list for the new paquet names 
    new_files = [] 
    
    # itirate through the parquet files and extract the date as string 
    for parquet in parquet_files: 
        filename = os.path.basename(parquet)
        df = dd.read_parquet(parquet, columns="Datetime").compute()
        parquet_new_name = str(df[1]).split(" ")[0] + ".parquet"
        
        # check for duplicate names (file already exist) --> save as duplicate
        if parquet_new_name in new_files:
            parquet_new_name = parquet_new_name.split(".")
            os.rename(parquet, parquets_directory_path + "/" + parquet_new_name[0] + "_duplicate." + parquet_new_name[1])
        else:
            new_files.append(parquet_new_name)
            os.rename(parquet, parquets_directory_path + "/" + parquet_new_name)
            
#################################################################

def connect_to_snowflake(username, password, account_name, role, warehouse, database, schema) -> "sql_connection":

    '''
    
    connects to snowflake dataframe and save the query data as dataframe
    
    parameters:
    ------------
    username: str
        username for the snowflake account
        
    password: str
        password for the snowflake account
        
    
    account_name: str
        can be found in the url-link. example: <account_name>.snowflakecomputing.com 
    
    warehouse: str
        name of the target warehouse
        
    database: str
        name of the target database
    
    schema: str
        name of the schema in the choosen database
    
    
    
    '''
    
    # pass the variable to the snowflake connector
    sql_connector = connector.connect(
    user = username, 
    password = password, 
    account = account_name, 
    role = role, 
    warehouse = warehouse, 
    database = database, 
    schema = schema
    )
    
    print(f"connection to database: {database} was successful")
    
    #create a connection to database
    sql_connection = sql_connector.cursor()
    
    return sql_connection


################################################################    
    
def query_snowflake(query , sql_connection)-> "pandas.Dataframe":
    
    '''
    excute sql query after connecting with a database    
        
    parameters:
    ----------
    
    query: str
        string form sql query that can be executed each line at a time 
    
    
    sql_connection: sql connection object
        object that is created after securing connection to a snowflake database
    

    '''
    
    connect = sql_connection.execute(query)
    
    dataframe = connect.fetch_pandas_all()
    
    
    if (dataframe.DATETIME.dtype == 'datetime64[ns, America/Los_Angeles]'):
        dataframe.DATETIME = dataframe.DATETIME.dt.tz_localize(None)
        print("zone code removed from time stamp")
        
    return dataframe

#########################################################


def check_features_for_sensor_error(features, dataframe)-> "Pandas.Series":
    
    '''
    
    Check if any of the features are responsible for the sensor error (-46,09)
    
    parameters:
    ----------
    
    features: list(str)
        list of all the columns that should be tested for -46,09 values
        
    dataframe: pandas.Dataframe
        pandas dataframe
    
    '''
    
    mydic = {}
    
    for feature in features:
        df = dataframe[dataframe[feature] == -46.09]
        error_records = len(df)
        mydic.update({feature : error_records})
    
    
    dic_to_series = pd.Series(mydic)
    
    return dic_to_series


#######################################

def check_features_for_logging_error(features, dataframe)-> "Pandas.Series":
    
    '''
    
    Check if any of the features are responsible for the logging error from data logger(-99.99)
    
    parameters:
    ----------
    
    features: list(str)
        list of all the columns that should be tested for -99,99 values
        
    dataframe: pandas.Dataframe
        pandas dataframe
    
    '''
    
    mydic = {}
    
    for feature in features:
        df = dataframe[dataframe[feature] == -99.99]
        error_records = len(df)
        mydic.update({feature : error_records})
    
    dic_to_series = pd.Series(mydic)
    
    return dic_to_series

#######################################


def remove_sensor_and_logging_errors(df) -> "Pandas.Dataframe":
    
    '''
    This function removes the sensor errors and logging errors from dataframe. 

    PS: The given dataframe should include a '99_Rows' and '46_Rows' columns
    '''
    try: 
        if not all(x in df.columns.to_list() for x in ["99_Rows" , "46_Rows"]):
            raise Exception("column '46_Rows' or '99_Rows' does not exist!")
    
        df = df.loc[df["99_Rows"]==0 , :]
        df = df.loc[df["46_Rows"]==0 , :]        
        
    except Exception as e:
        print(e)
    
    else:
        print("** Number of logging errors in each of the following features:\n")
        no_logging_errors = check_features_for_logging_error([x for x in df.columns if x not in ["99_Rows" , "46_Rows"]], df)
        print(no_logging_errors)
        
        print("--------------------------------------------------------------")
        
        print("** Number of sensor errors in each of the following features:\n")
        no_sensor_errors = check_features_for_sensor_error([x for x in df.columns if x not in ["99_Rows" , "46_Rows"]], df)
        print(no_sensor_errors)
        
        return df 
    
    
    
#######################################################################################

def highlight_missing_data(dataframe, signal, freq , axis=None)-> "Figure":
    
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
    
    
    fig, ax = plt.subplots(figsize=(20,5))
    
    # first figure 
    ax.plot(df_with_nan_values.index , df_with_nan_values[signal])
    
    # second figure
    ax.fill_between(x=df_imputed.index,
                     y1=0,
                     y2= max_signal,
                     where = df_imputed[signal] == max_signal, color="r" , alpha=0.15)
    return plt.gcf()

    
######################################################################################
    
    
def number_of_missing_values(df , freq)->"None":
    
    '''
    This finction checks the number of missing values (NaN) in a dataframe in form of numbers and percentage
    
    
    
    Parameters:
    ----------
    
    df: Pandas.Dataframe
        A panda dataframe that contains the required features to inspect for missing values (NaN)
    
    freq: str
        The frequency of the timestamp in the dataframe 
        exple: "S" for one second , "T" for one minute , "10T" for ten minutes
        
    '''    
    
    df_zeros = df.asfreq(freq)  #New dataframe with same frequency as the original to expose the NaN values
    
    result_values = df_zeros.isna().sum() #Number of NaN values
    
    result_percentage = round( (result_values/len(df_zeros))*100 , 2)  #Calcutae percentage and round to two numbers only
    
    result_percentage_str = result_percentage.astype("string") + "  " + "%"  #Convert to string and add "%" sign 
    
    
    print("Number of NaN values in each column:")
    print("------------------------------------")
    print(result_values)
    
    print("\n")
    
    print("Number of NaN percentage in each column:")
    print("----------------------------------------")
    print(result_percentage_str)
    
    
        