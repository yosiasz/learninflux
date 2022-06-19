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

bucket = "winds"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(URL="http://localhost:8086", token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["windgust","windspeed","winddir","datetime"]
df = pd.read_csv("./data/winds.csv", usecols=col_list)

for index, row in df.iterrows():
    windgust =  float(row['windgust'])
    windspeed =  float(row['windspeed'])
    winddir =  int(row['winddir'])
    recordedtime = row['datetime']

    point = Point("weather") \
            .tag("type", "winds") \
            .field("windgust", windgust) \
            .field("windspeed", windspeed) \
            .field("winddir", winddir) \
            .time(recordedtime, WritePrecision.NS)

    write_api.write(bucket, org, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
