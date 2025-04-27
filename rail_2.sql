CREATE TABLE rail_2 AS (
    SELECT  A.name AS from_stop,B.name AS to_stop,rail_1.route_name,rail_1.d,rail_1.duration_avg,rail_1.n_vehicles,rail_1.route_i_counts
    FROM rail_1,table_stops1 as A,table_stops1 as B
    WHERE rail_1.from_stop_i=A.stop_id AND rail_1.to_stop_i=B.stop_id
)
