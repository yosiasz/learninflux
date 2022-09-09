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

bucket = "sel"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["MARKER","STATUS","_field","_measurement","value"]
df = pd.read_csv("./data/selenium.csv", usecols=col_list)

#48°30'06.9"N 11°57'46.6"E

for index, row in df.iterrows():   
    _measurement =  row['_measurement']
    MARKER = row['MARKER']
    STATUS = row['STATUS']

    point = Point('test_execution') \
            .field('MARKER', MARKER) \
            .field('BUILD_NUMBER',1) \
            .field('STATUS',STATUS) \
            .time( datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
