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

bucket = "ships"
filename = './data/ships.csv'

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

#Time,AntLat,AntLong,DraghSBLat,DraghSBLong,Total
col_list = ["Time","AntLat","AntLong","DraghSBLat","DraghSBLong","Total"]
df = pd.read_csv(filename, usecols=col_list)

for index, row in df.iterrows():
    time =  row['Time']
    antennalatitude = float(row['AntLat'])
    antennalongitude = float(row['AntLong'])
    dragheadsblatitude = float(row['DraghSBLat'])
    dragheadsblongitude = float(row['DraghSBLong'])
    total = float(row['Total'])

    point = Point("ship") \
            .measurement("locations") \
            .tag("type", "dredgeview") \
            .field("antennalatitude", antennalatitude) \
            .field("antennalongitude", antennalongitude) \
            .field("dragheadsblatitude", dragheadsblatitude) \
            .field("dragheadsblongitude", dragheadsblongitude) \
            .field("total", total) \
            .time(time, WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
