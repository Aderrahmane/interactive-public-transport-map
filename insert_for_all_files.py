import csv
import psycopg2

def generate_insert_sql(input_file, output_sql_file):
    with open(input_file, 'r') as f, open(output_sql_file, 'w') as output_file:
        next(f)

        for line in f:
            items = line.rstrip("\n").split(";")

            num_attributes = len(items)

            i = 0
            insert_line = f"INSERT INTO bus VALUES ("
            while i < num_attributes:
                item = items[i].replace("'", "''")
                insert_line = insert_line + "'" + item + "'"
                if i != num_attributes - 1:
                    insert_line = insert_line + ", "
                i = i + 1

            insert_line = insert_line + ");"
            print(insert_line, file=output_file)

def execute_sql_file(sql_file, db_params):
    try:
        # Open a connection to the database
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Execute the SQL file
        with open(sql_file, 'r') as file:
            cursor.execute(file.read())

        # Commit the changes to the database
        connection.commit()
        print(f"SQL file '{sql_file}' executed successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # List of input CSV files
    input_files = ["network_bus.csv", "another_file.csv", "yet_another_file.csv"]

    # Common database connection parameters
    db_params = {
        'host': 'your_host',
        'database': 'your_database',
        'user': 'your_user',
        'password': 'your_password'
    }

    for input_file in input_files:
        # Generate SQL file for each input file
        output_sql_file = f"{input_file.split('.')[0]}_output.sql"
        generate_insert_sql(input_file, output_sql_file)

        # Execute SQL file for each input file
        execute_sql_file(output_sql_file, db_params)
