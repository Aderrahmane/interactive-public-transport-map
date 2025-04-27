CREATE TABLE tram_2 AS (
    SELECT  A.name AS from_stop,B.name AS to_stop,tram_1.route_name,tram_1.d,tram_1.duration_avg,tram_1.n_vehicles,tram_1.route_i_counts
    FROM tram_1,table_stops1 as A,table_stops1 as B
    WHERE tram_1.from_stop_i=A.stop_id AND tram_1.to_stop_i=B.stop_id
)
