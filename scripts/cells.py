import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL')
ORG = os.getenv('ORG')

bucket = "electric_boogaloo"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["device","current","timestamp"]
df = pd.read_csv("./data/cells.csv", usecols=col_list)

for index, row in df.iterrows():
    device =  row['device']
    current = int(row['current'])
    timestamp = row['timestamp']

    point = Point("solarpanel") \
            .measurement(device) \
            .field("current", current) \
            .time(timestamp, WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()