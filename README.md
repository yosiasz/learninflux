a repository of my learning journey with influxdb

https://json-generator.com/

[
  '{{repeat(1025)}}',
  {
    _id: '{{objectId()}}',
    name: '{{lorem(1, "words")}}',
    balance: '{{integer(100, 999)}}'
  }
]

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
influx config create -a -n research -u http://localhost:8086 -t TOKEN -o ORG

--Convert db
influx v1 dbrp create --bucket-id f4a5f1ee338536fd --db switches-db --rp switches-rp --default --o research -t TOKEN

influx v1 dbrp create --bucket-id 8af0ae6d56a8e97e --db 1-wire-db --rp 1-wire-rp --default --o research -t TOKEN

influx v1 dbrp create --bucket-id f4a5f1ee338536fd --db switches-db --rp switches-rp --default --org-id e966b28df9baf9c6 -t TOKEN

influx v1 dbrp create --bucket-id 8a92664b58535f51 --db venus_default-db --rp venus_default-rp --default

SELECT "ifDescr", "ifOperStatus" FROM "switches-rp"."autogen" WHERE $timeFilter and "ifOperStatus" != 2 and  "ifOperStatus" != 6 