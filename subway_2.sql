CREATE TABLE subway_2 AS (
    SELECT  A.name AS from_stop,B.name AS to_stop,subway_1.route_name,subway_1.d,subway_1.duration_avg,subway_1.n_vehicles,subway_1.route_i_counts
    FROM subway_1,table_stops1 as A,table_stops1 as B
    WHERE subway_1.from_stop_i=A.stop_id AND subway_1.to_stop_i=B.stop_id
)
