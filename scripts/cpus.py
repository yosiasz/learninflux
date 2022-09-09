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

bucket = "cpus"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["readdate","cpu"]
df = pd.read_csv("./data/cpus.csv", usecols=col_list)
time =  datetime.utcnow() #row['Time']

for index, row in df.iterrows():
    readdate =  row['readdate']
    cpu =  float(row['cpu'])

    point = Point("cpus") \
            .tag("type", "perf") \
            .field("cpu", cpu) \
            .time( readdate, WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
