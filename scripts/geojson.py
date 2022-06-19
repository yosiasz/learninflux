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
bucket = "map"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["Time","sensor","lonE","latE"]
df = pd.read_csv("./data/geojson.csv", usecols=col_list)

for index, row in df.iterrows():
    #print(row)
    lonE =  row['lonE']
    latE =  row['latE']
    sensor = row['sensor']
    recordedtime = row['Time']

    point = Point("zoo") \
            .tag("type", "za") \
            .field("sensor", sensor) \
            .field("lonE", lonE) \
            .field("latE", latE) \
            .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, org, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
