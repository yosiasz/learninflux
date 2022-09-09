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

bucket = "1-wire"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["host","process","status","dtime"]
df = pd.read_csv("./data/1-wire.csv", usecols=col_list)

for index, row in df.iterrows():
    host =  row['host']
    serverrack8 =  int(row['serverrack8'])
    serverrack10 =  int(row['serverrack10'])    
    dtime =  row['serverrack10']

    point = Point("1-wire") \
            .tag("type", "1-wire") \
            .field("host", host) \
            .field("serverrack8", serverrack8) \
            .field("serverrack10", serverrack10) \
            .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
