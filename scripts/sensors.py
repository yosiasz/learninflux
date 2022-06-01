import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

org = "research"
bucket = "sensors"
filename = './data/sensors.csv'

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url="http://localhost:8086", token=token, org=org, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["sensorname","timeline","humidity","lat","lng"]
df = pd.read_csv(filename, usecols=col_list)

for index, row in df.iterrows():
    sensorname =  row['sensorname']
    humidity =  float(row['humidity'])
    lat =  float(row['lat'])
    lng =  float(row['lng'])

    json_body1 = [
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
                    "humidity": humidity
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
    write_api.write(bucket, org, json_body) 
    write_api.__del__()

"""
Close client
"""
client.__del__()
