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
influx config create --config-name mygrafana --host-url http://localhost:3000 --org Research --token f9fZzCjNyZsVm9mCgZZh6tkyeazTelyZJbp2bypq-dzS1_DTQNxce7cKwMrDRGjEvHig-3OVmJVoGbQnVY_4gA== --active

--Convert db
influx v1 dbrp create --bucket-id f4a5f1ee338536fd --db switches-db --rp switches-rp --default --o research -t f9fZzCjNyZsVm9mCgZZh6tkyeazTelyZJbp2bypq-dzS1_DTQNxce7cKwMrDRGjEvHig-3OVmJVoGbQnVY_4gA==

influx v1 dbrp create --bucket-id f4a5f1ee338536fd --db switches-db --rp switches-rp --default --org-id e966b28df9baf9c6 -t f9fZzCjNyZsVm9mCgZZh6tkyeazTelyZJbp2bypq-dzS1_DTQNxce7cKwMrDRGjEvHig-3OVmJVoGbQnVY_4gA==

influx v1 dbrp create --bucket-id 8a92664b58535f51 --db venus_default-db --rp venus_default-rp --default

SELECT "ifDescr", "ifOperStatus" FROM "switches-rp"."autogen" WHERE $timeFilter and "ifOperStatus" != 2 and  "ifOperStatus" != 6 