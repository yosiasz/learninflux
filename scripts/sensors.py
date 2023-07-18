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

bucket = "sensors"
filename = './data/sensors_clean.csv'

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url="http://localhost:8086", token="dUREU8fceyXlT5z8yGuxzAj_EvWx89eZbhviGPwPILjWqR88NW1OP5xYRcmvKBMjwxxLbniJk5YQu13gyaL4LQ==",org="research", debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

#col_list = ["sensorname","timeline","humidity","lat","lng","state_name"]
col_list =["measurement","device","temptype","celcius","fahrenheit","datetime"]
df = pd.read_csv(filename, usecols=col_list)

for index, row in df.iterrows():

    """ json_body1 = [
        {
            "measurement": "sensor_readings",
            "tags": {
                "latitude": lat,
                "longitude": lng
            },
            "time": datetime.utcnow(),
            "fields": {
                "sensorname": sensorname,
                "humidity": humidity
            }
        }
    ]

    json_body = [
            {
                "measurement": "sensor_readings",
                "time": datetime.utcnow(),
                "fields": {
                    "latitude": lat,
                    "longitude": lng,
                    "sensorname": sensorname,
                    "humidity": humidity,
                    "state_name": state_name,
                }
            }
        ]
 """
    measurement =  row['measurement']
    device =  row['device']
    temptype =  row['temptype']
    celcius =  float(row['celcius'])
    fahrenheit = float(row['fahrenheit'])
    datetime = row['datetime']

    json_body3 = [
            {
                "measurement": measurement,
                "time": datetime,
                "fields": {
                    "temptype": temptype,
                    "celcius": celcius,
                    "fahrenheit": fahrenheit
                }
            }
        ]        
    """     
    point = Point("sensors") \
            .measurement("sensor_readings") \
            .tag("Latitude", lat) \
            .tag("Longitude", lng) \
            .field("sensorname ", sensorname) \
            .field("humidity ", humidity) \
            .time(datetime.utcnow(), WritePrecision.NS) """
    #client.write_points(json_body)
    write_api.write(bucket, "research", json_body3) 
    write_api.__del__()

"""
Close client
"""
client.__del__()
