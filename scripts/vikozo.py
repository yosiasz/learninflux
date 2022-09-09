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

bucket = "vikozo"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["time","bytes_recv","bytes_sent","interface"]
df = pd.read_csv("./data/vikozo.csv", usecols=col_list)
time =  datetime.utcnow() #row['Time']

for index, row in df.iterrows():
    bytes_recv =  int(row['bytes_recv'])
    bytes_sent =  int(row['bytes_sent'])
    interface =  row['interface']

    point = Point("packets") \
            .tag("interface", interface) \
            .field("bytes_recv", bytes_recv) \
            .field("bytes_sent", bytes_sent) \
            .time(time, WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
