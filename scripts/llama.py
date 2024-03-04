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

bucket = "llama"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

#qsys_core_info,name=QSYS001,source=10.37.155.161 version="9.8.2-2308.002" 1707874158000000000
#11111111,0.8,458.1,40.4665013,13.513669566666668,1i,6i,0
for next_ip in range(10):
    point = Point("llama") \
            .measurement("qsys_core_info") \
            .tag("name", "QSYS002") \
            .field("source", "10.37.155.16" + str(next_ip)) \
            .field("version", "9.8.2-2308.00" + str(next_ip)) \
            .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()