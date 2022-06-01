import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# You can generate an API token from the "API Tokens Tab" in the UI
#Token f9fZzCjNyZsVm9mCgZZh6tkyeazTelyZJbp2bypq-dzS1_DTQNxce7cKwMrDRGjEvHig-3OVmJVoGbQnVY_4gA==
token ="f9fZzCjNyZsVm9mCgZZh6tkyeazTelyZJbp2bypq-dzS1_DTQNxce7cKwMrDRGjEvHig-3OVmJVoGbQnVY_4gA=="

org = "research"
bucket = "bitrates"
filename = './data/bitrates.csv'

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url="http://localhost:8086", token=token, org=org, debug=True)
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
