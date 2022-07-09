import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')
ORG = os.getenv('ORG')

bucket = "win_services"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["host","startup_mode","state","display_name","service_name","startup_mode"]
df = pd.read_csv("./data/winservices.csv", usecols=col_list)

for index, row in df.iterrows():
    #somehost,2i,4i,sync\ Host8F9a08F98,One_sync_service8F9a08F98,2i
    host =  row['host']
    startup_mode =  row['startup_mode']
    state =  row['state']
    display_name = row['display_name']
    service_name = row['service_name']
    startup_mode = row['startup_mode']

    point = Point("win_services") \
            .tag("type", "win_services") \
            .field("host", host) \
            .field("startup_mode", startup_mode) \
            .field("state", state) \
            .field("display_name", display_name) \
            .field("service_name", service_name) \
            .field("startup_mode", startup_mode) \
            .time( datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
