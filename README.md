a repository of my learning journey with influxdb

parse-json
| scope "Countries"
| jsonata "*[Country="Australia"]"
#| json {Countries.Country= 'Afghanistan'}
#| jsonata "*[Country:"Australia"]"
#| jsonata "*[date>=${__from:date:seconds} and date<=${__to:date:seconds}]"
#| jsonata { 'Country'= "Australia"} 
#| jsonata { 'Country': "Australia"} 
#| jsonata "$[Country=\"Australia\"]"
#| jsonata "$[`Start date`=\"${__from:date:DD/MM/YYYY}\"]"
#| jsonata "$[`Country`='Australia']"
#| jsonata "({'Country' : "Australia"})"
#| jsonata "Countries.Country = 'Australia'"
#jsonata "$[`Start date`='11/05/2022']"

--Create config (saved C:\Users\Josiah Solomon\.influxdbv2)
```
influx config create --config-name mygrafana --host-url http://localhost:3000 --org Research --token TOKEN --active

--Convert db
influx v1 dbrp create --bucket-id f4a5f1ee338536fd --db switches-db --rp switches-rp --default 
```

