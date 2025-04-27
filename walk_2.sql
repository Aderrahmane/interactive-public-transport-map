CREATE TABLE walk_2 AS (
    SELECT  A.name AS from_stop,B.name AS to_stop,walk.d,walk.d_walk
    FROM walk,table_stops1 as A,table_stops1 as B
    WHERE walk.from_stop_i=A.stop_id AND walk.to_stop_i=B.stop_id
)
