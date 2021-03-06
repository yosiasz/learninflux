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

bucket = "bitrates"
filename = './data/bitrates.csv'

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

#hostname,ifiInBits_rate
col_list = ["hostname","ifiInBits_rate"]
df = pd.read_csv(filename, usecols=col_list)

for index, row in df.iterrows():
    hostname =  row['hostname']
    ifiInBits_rate = int(row['ifiInBits_rate'])
    
    point = Point("analysis") \
            .measurement("tput") \
            .tag("type", "networkbirates") \
            .field("hostname", hostname) \
            .field("ifiInBits_rate", ifiInBits_rate) \
            .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, org, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()
