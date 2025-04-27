CREATE TABLE combined_table AS
SELECT DISTINCT ON (from_stop, to_stop)
    from_stop,
    to_stop,
    bus_d,
    bus_route_name,
    bus_duration_avg,
    rail_d,
    rail_route_name,
    rail_duration_avg,
    subway_d,
    subway_route_name,
    subway_duration_avg,
    tram_d,
    tram_route_name,
    tram_duration_avg,
    walk_d,
    walk_route_name,
    walk_duration_avg
FROM (
    SELECT
        CASE WHEN b.from_stop <= b.to_stop THEN b.from_stop ELSE b.to_stop END AS from_stop,
        CASE WHEN b.from_stop <= b.to_stop THEN b.to_stop ELSE b.from_stop END AS to_stop,
        b.d AS bus_d,
        b.route_name AS bus_route_name,
        b.duration_avg AS bus_duration_avg,
        r.d AS rail_d,
        r.route_name AS rail_route_name,
        r.duration_avg AS rail_duration_avg,
        s.d AS subway_d,
        s.route_name AS subway_route_name,
        s.duration_avg AS subway_duration_avg,
        t.d AS tram_d,
        t.route_name AS tram_route_name,
        t.duration_avg AS tram_duration_avg,
        w.d AS walk_d,
        NULL AS walk_route_name,
        w.d_walk AS walk_duration_avg
    FROM bus_2 b
    FULL JOIN rail_2 r ON b.from_stop = r.from_stop AND b.to_stop = r.to_stop
    FULL JOIN subway_2 s ON b.from_stop = s.from_stop AND b.to_stop = s.to_stop
    FULL JOIN tram_2 t ON b.from_stop = t.from_stop AND b.to_stop = t.to_stop
    FULL JOIN walk_2 w ON b.from_stop = w.from_stop AND b.to_stop = w.to_stop

    UNION

    SELECT
        CASE WHEN b.from_stop <= b.to_stop THEN b.from_stop ELSE b.to_stop END AS from_stop,
        CASE WHEN b.from_stop <= b.to_stop THEN b.to_stop ELSE b.from_stop END AS to_stop,
        NULL AS bus_d,
        NULL AS bus_route_name,
        NULL AS bus_duration_avg,
        NULL AS rail_d,
        NULL AS rail_route_name,
        NULL AS rail_duration_avg,
        NULL AS subway_d,
        NULL AS subway_route_name,
        NULL AS subway_duration_avg,
        NULL AS tram_d,
        NULL AS tram_route_name,
        NULL AS tram_duration_avg,
        w.d AS walk_d,
        NULL AS walk_route_name,
        w.d_walk AS walk_duration_avg
    FROM walk_2 w
    LEFT JOIN bus_2 b ON b.from_stop = w.from_stop AND b.to_stop = w.to_stop
    LEFT JOIN rail_2 r ON r.from_stop = w.from_stop AND r.to_stop = w.to_stop
    LEFT JOIN subway_2 s ON s.from_stop = w.from_stop AND s.to_stop = w.to_stop
    LEFT JOIN tram_2 t ON t.from_stop = w.from_stop AND t.to_stop = w.to_stop
) AS subquery;
