
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
