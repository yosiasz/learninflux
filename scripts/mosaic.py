import json
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL')
ORG = os.getenv('ORG')
bucket = "mosaic"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["Time","sensor","lonE","latE"]
f = open('./data/mosaic.json')
data = json.load(f)

for i in data:
    breakdown =  i['Breakdown']
    amplitude =  int(i['Amplitude'])
    readingdate =  i['readingdate']

    point = Point("mozaic") \
            .tag("type", "readings") \
            .field("Breakdown", breakdown) \
            .field("Amplitude", amplitude) \
            .time(readingdate, WritePrecision.NS)

    write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
# Closing file
f.close()
client.__del__()
