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

bucket = "switches"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["Time","ifDescr","ifOperStatus"]
df = pd.read_csv("./data/switches.csv", usecols=col_list)
time =  datetime.utcnow() #row['Time']

for index, row in df.iterrows():
    ifDescr =  row['ifDescr']
    ifOperStatus =  int(row['ifOperStatus'])

    point = Point("autogen") \
            .tag("type", "switch") \
            .field("ifDescr", ifDescr) \
            .field("ifOperStatus", ifOperStatus) \
            .time( datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
