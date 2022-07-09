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

bucket = "cars"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["carId","state","timestamp"]
df = pd.read_csv("./data/cars.csv", usecols=col_list)

for index, row in df.iterrows():
    carId =  int(row['carId'])
    state = int(row['state'])
    timestamp = row['timestamp']

    point = Point("carfleet") \
            .measurement("tput") \
            .tag("carId", carId) \
            .field("state", state) \
            .time(timestamp, WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()