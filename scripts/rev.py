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

bucket = "bucket"
filename = './data/rev.csv'

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

#Time,AntLat,AntLong,DraghSBLat,DraghSBLong,Total
col_list = ["uic","gps_hdop","gps_height","gps_latitude","gps_longitude","gps_quality","gps_satellites","gps_speed"]
df = pd.read_csv(filename, usecols=col_list)
#11111111,0.8,458.1,40.4665013,13.513669566666668,1i,6i,0
for index, row in df.iterrows():
    uic = row['uic']
    gps_hdop = float(row['gps_hdop'])
    gps_height = float(row['gps_height'])
    gps_latitude = float(row['gps_latitude'])
    gps_longitude = float(row['gps_longitude'])
    gps_quality = row['gps_quality']
    gps_satellites = row['gps_satellites']
    gps_speed = row['gps_speed']

    point = Point("truck_trackers") \
            .measurement("car") \
            .tag("type", "donde_es_mi_caro") \
            .field("uic", uic) \
            .field("gps_hdop", gps_hdop) \
            .field("gps_height", gps_height) \
            .field("gps_latitude", gps_latitude) \
            .field("gps_longitude", gps_longitude) \
            .field("gps_quality", gps_quality) \
            .field("gps_satellites", gps_satellites) \
            .field("gps_speed", gps_speed) \
            .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()


""" from(bucket: "bucket")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "loco")
  |> filter(fn: (r) => r["uic"] == "11111111 ")
  |> filter(fn: (r) => r["_field"] == "gps_latitude" or r["_field"] == "gps_longitude" or r["_field"] == "gps_speed")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean") """