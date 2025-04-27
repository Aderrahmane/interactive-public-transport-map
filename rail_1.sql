CREATE TABLE rail_1 AS (
    SELECT rail.*,route_name_stop_1.route_name
    FROM rail,route_name_stop_1
    WHERE rail.from_stop_i=route_name_stop_1.from_stop_i AND rail.to_stop_i=route_name_stop_1.to_stop_i AND route_name_stop_1.route_type='2'
)