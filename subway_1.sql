CREATE TABLE subway_1 AS (
    SELECT  subway.*,route_name_stop_1.route_name
    FROM subway,route_name_stop_1
    WHERE subway.from_stop_i=route_name_stop_1.from_stop_i AND subway.to_stop_i=route_name_stop_1.to_stop_i AND route_name_stop_1.route_type='1'
)