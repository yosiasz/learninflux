
pivoted = from(bucket: "sel")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "test_execution")  
  |> pivot(rowKey:["_time"], columnKey: ["_value"], valueColumn: "_field")
  |> group(columns: ["MARKER"])  
  |> drop(columns: ["_start", "_stop", "_measurement"])

pivoted  


from(bucket: "cpus")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "cpus")
  |> filter(fn: (r) => r["_field"] == "cpu")
  |> filter(fn: (r) => r["type"] == "perf")
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")  
  |> drop(columns: ["_start", "_stop", "_measurement", "type"])
