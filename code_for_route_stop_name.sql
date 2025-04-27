CREATE TABLE route_name_stop AS (
SELECT from_stop_i, to_stop_i,route_type,route_i
FROM network_temp
)