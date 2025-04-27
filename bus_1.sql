CREATE TABLE bus_1 AS (
    SELECT  bus.*,route_name_stop_1.route_name
    FROM bus,route_name_stop_1
    WHERE bus.from_stop_i=route_name_stop_1.from_stop_i AND bus.to_stop_i=route_name_stop_1.to_stop_i AND route_name_stop_1.route_type='3'
)