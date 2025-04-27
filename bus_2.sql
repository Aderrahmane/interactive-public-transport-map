CREATE TABLE bus_2 AS (
    SELECT A.name AS from_stop,B.name AS to_stop,bus_1.route_name,bus_1.d,bus_1.duration_avg,bus_1.n_vehicles,bus_1.route_i_counts
    FROM bus_1,table_stops1 as A,table_stops1 as B
    WHERE bus_1.from_stop_i=A.stop_id AND bus_1.to_stop_i=B.stop_id
)
