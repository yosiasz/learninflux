InfluxQL 
    1. Convert to db
        influx v1 dbrp create --bucket-id 50e00483c591b07b --db bitrate-db --rp bitrate-rp -o Research -t -mdsRNQxQOoaUESel9FLnDCXlo5kF_OnxSLS334hEJyXFSzoh07y6iGoZuRJnuMOKGXhR_Sq43P6EsOmShGV0A==
    2. Test
    curl --get http://localhost:8086/query?db=example-db --header "Authorization: Token -mdsRNQxQOoaUESel9FLnDCXlo5kF_OnxSLS334hEJyXFSzoh07y6iGoZuRJnuMOKGXhR_Sq43P6EsOmShGV0A==" --data-urlencode "q=SELECT * FROM bitrate-db WHERE host=bitpos"

https://influxdb-python.readthedocs.io/en/latest/examples.html