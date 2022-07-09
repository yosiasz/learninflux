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

bucket = "process"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["host","process","status","dtime"]
df = pd.read_csv("./data/1-wire.csv", usecols=col_list)

for index, row in df.iterrows():
    host =  row['host']
    process =  row['process']
    status =  row['status']
    dtime =  row['dtime']

    point = Point("boojee") \
            .tag("type", "statuses") \
            .field("process", process) \
            .field("status", status) \
            .time(dtime, WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
