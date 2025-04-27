CREATE TABLE tram_1 AS (
    SELECT  tram.*,route_name_stop_1.route_name
    FROM tram,route_name_stop_1
    WHERE tram.from_stop_i=route_name_stop_1.from_stop_i AND tram.to_stop_i=route_name_stop_1.to_stop_i AND route_name_stop_1.route_type='0'
)