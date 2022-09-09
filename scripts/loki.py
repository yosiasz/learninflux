import datetime
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

bucket = "CSV"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["date","key0","key1"]
df = pd.read_csv("./data/loki.csv", usecols=col_list)
time =  datetime.utcnow() #row['Time']

for index, row in df.iterrows():
    date =  row['date']
    dt2 = datetime.strptime(date, "%Y%m%dt%H%M%S")
    dt = pd.to_datetime(date, format='%Y%m%dt%H%M%S', errors='ignore')

    print(dt)

    
    key0 =  int(row['key0'])
    key1 =  float(row['key1'])

    point = Point("fakeloki") \
            .tag("type", "perf") \
            .field("key0", key0) \
            .field("key1", key1) \
            .time( dt, WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
