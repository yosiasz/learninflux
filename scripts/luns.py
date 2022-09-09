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

bucket = "luns"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["_measurement","dev","lun","Tot_Rsvd","VSize","_time"]
df = pd.read_csv("./data/lun.csv", usecols=col_list)

#48°30'06.9"N 11°57'46.6"E

for index, row in df.iterrows():   
    _time =  row['_time']
    lun =  row['lun']
    dev =  row['dev']
    Tot_Rsvd = int(row['Tot_Rsvd'])
    VSize = int(row['VSize'])
    _measurement =  row['_measurement']
    

    point = Point("cpubar") \
            .tag("type", "cpu") \
            .field("lun", lun) \
            .field("Tot_Rsvd", Tot_Rsvd) \
            .field("VSize", VSize) \
            .time(datetime.utcnow(), WritePrecision.NS)
            #.time(_time, WritePrecision.NS)

    point2 = Point(_measurement) \
            .tag("lun", lun) \
            .tag("dev", dev) \
            .tag("Tot_Rsvd", Tot_Rsvd) \
            .tag("VSize", VSize) \
            .time(_time, WritePrecision.NS)
            
    print(lun)             
    write_api.write(bucket, ORG, point) 
    #write_api.write(bucket, ORG, point2) 
write_api.__del__()

"""
Close client
"""
client.__del__()
