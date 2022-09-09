
/*

result,table,_start,_stop,_time,appliance,_value
my-result,0,2018-05-08T20:50:00Z,2018-05-08T20:51:00Z,2018-05-08T20:50:00Z,toaster,15.43
my

table,_start,_stop,_time,_value,_field,_measurement,uic

*/

;with src
as
(
SELECT TOP (50)        
		--'mqtt_consumer' as _measurement,
        id   = ISNULL(CAST(
                          ROW_NUMBER() OVER (ORDER BY (SELECT 1))
                       AS INT),0)
   FROM master.sys.all_columns ac1
  CROSS JOIN master.sys.all_columns ac2
  CROSS JOIN master.sys.all_columns ac3
)

SELECT dateadd(hh, id, getdate()) as _time,
       --id * 1.32 as _value ,
	   ROUND(RAND(CHECKSUM(NEWID())) * (100), 2) as _value

		--,_measurement
   FROM src
   --cross apply (select 'Toaster' as _field union select 'Kettle' union select 'Oven' union select 'Microwave' union select 'Washing machine') a