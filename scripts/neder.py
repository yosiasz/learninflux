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

bucket = "nederland"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["temp","time"]
df = pd.read_csv("./data/nederland.csv", usecols=col_list)

#48°30'06.9"N 11°57'46.6"E

for index, row in df.iterrows():   
    temp =  float(row['temp'])
    time =  row['time']    

    point = Point("temps") \
            .tag("type", "temp") \
            .field("temp", temp) \
            .time(time, WritePrecision.NS)

    write_api.write(bucket, ORG, point)
write_api.__del__()

"""
Close client
"""
client.__del__()
