import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from dotenv import load_dotenv
import os
import numpy as np
import sqlite3
from sqlite3 import Error

load_dotenv()

TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL')
ORG = os.getenv('ORG')
bucket = "spectrum"

h = 6.626e-34
c = 3.0e+8
k = 1.38e-23

def write_data_to_bucket():
    """
    Write data into InfluxDB
    """
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
    write_api = client.write_api(write_options=SYNCHRONOUS)  

    col_list = ["Red","Green","Blue","Temperature"]
    df = pd.read_csv("./data/spectrum.csv", usecols=col_list)
    time =  datetime.utcnow() #row['Time']

    for index, row in df.iterrows():
        Red =  int(row['Red'])
        Green =  int(row['Green'])
        Blue =  int(row['Blue'])
        Temperature =  int(row['Temperature'])

        point = Point("spectrum") \
                .tag("type", "wave") \
                .field("Red", Red) \
                .field("Green", Green) \
                .field("Blue", Blue) \
                .field("Temperature", Temperature) \
                .time( datetime.utcnow(), WritePrecision.NS)

        write_api.write(bucket, ORG, point) 
    write_api.__del__()

    """
    Close client
    """
    client.__del__()

def planck(wav, T):
    a = 2.0*h*c**2
    b = h*c/(wav*k*T)
    intensity = a/ ( (wav**5) * (np.exp(b) - 1.0) )
    return intensity

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_data(conn, data):
    """
    Create a new project into the projects table
    :param conn:
    :param data:
    :return: data id
    """
    cur = conn.cursor()
    
    #check_table_exists = ''' SELECT name FROM sqlite_master WHERE type='table' AND name='spectrum' ''';

    #tableExists = cur.execute(check_table_exists)
    
    #cur.execute("CREATE TABLE spectrum(Red, Green, Blue, Temperature )")    

    sql = ''' INSERT INTO spectrum(Red, Green, Blue, Temperature)
              VALUES(?,?,?,?) '''
    
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid

def create_spectrum(conn):
    # generate x-axis in increments from 1nm to 3 micrometer in 1 nm increments
    # starting at 1 nm to avoid wav = 0, which would result in division by zero.
    #wavelengths = np.arange(1e-9, 3e-6, 1e-9) 
    #114, 150,224,5085
    #wv  640nm, 524nm and 470nm
    # intensity at 4000K, 5000K, 6000K, 7000K
    wavelengths = np.arange(640, 524, 470) 
    i1 = planck(wavelengths, 5085.)
    i2 = planck(wavelengths, 5085.)
    i3 = planck(wavelengths, 5085.)

    data = (i1,i2,i3);

    """
    Create a new project into the projects table
    :param conn:
    :param data:
    :return: data id
    """
    cur = conn.cursor()
    
    #check_table_exists = ''' SELECT name FROM sqlite_master WHERE type='table' AND name='spectrum' ''';

    #tableExists = cur.execute(check_table_exists)
    
    cur.execute("CREATE TABLE blackbody(i1, i2, i3, i4 )")    

    sql = ''' INSERT INTO blackbody(i1, i2, i3)
              VALUES(?,?,?) '''
    
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid

def main():
    database = r"C:\myapps\grafana-helper\src\data\blackbody.db"

    # create a database connection
    conn = create_connection(database)

    with conn:
        data_id = create_spectrum(conn)

if __name__ == '__main__':
    main()
