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

bucket = "ping"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["_measurement","url","time","cpu","average_response_ms"]
df = pd.read_csv("./data/polystat.csv", usecols=col_list)

for index, row in df.iterrows():   
    _time =  row['time']
    _value =  float(row['average_response_ms'])
    _measurement =  row['_measurement']
    _url = row['url']

    point = Point(_measurement) \
            .field('average_response_ms', _value) \
            .field('url', _url) \
            .time(_time, WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
