CREATE TABLE route_name_stop_1 AS (
    SELECT route_name_stop.*,routes.route_name
    FROM route_name_stop,routes
    WHERE route_name_stop.route_i=routes.route_i AND routes.route_type=route_name_stop.route_type
)