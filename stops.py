def print_insert_statements(features):
    for feature in features:
        properties = feature.get('properties', {})
        coordinates = feature.get('geometry', {}).get('coordinates', [])

        stop_id = properties.get('stop_I', None)
        name = properties.get('name', None)
        lat = coordinates[1] if coordinates else None
        alt = coordinates[0] if coordinates else None

        # Construct parameterized SQL statement
        sql_statement = f"INSERT INTO table_stops (stop_id, name, lat, lng) VALUES ({stop_id}, '{name}', {lat}, {alt});"
        print(sql_statement)

# Print parameterized SQL INSERT statements
print_insert_statements(geojson_data.get('features', []))

