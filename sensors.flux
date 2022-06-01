
from(bucket: "sensors")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "sensor_readings")
  |> filter(fn: (r) => r._field == "humidity" or r._field == "sensorname" or r._field == "longitude" or r._field == "latitude")  
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> group()  
  |> drop(columns: ["_start", "_stop", "_time","_measurement"])