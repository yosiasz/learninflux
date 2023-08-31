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

bucket = "electric_boogaloo"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["cellname","voltage"]
df = pd.read_csv("./data/cells.csv", usecols=col_list)

for index, row in df.iterrows():
    cellname =  row['cellname']
    voltage = int(row['voltage'])

    point = Point("power_usage") \
            .measurement(cellname) \
            .tag("cellname", cellname) \
            .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()