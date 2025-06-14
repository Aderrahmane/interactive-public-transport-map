import csv

# Write INSERT statements to the terminal
with open("Paris-routeI-routeName-routeType(1).csv", 'r') as f:
    next(f)

    for line in f:
        items = line.rstrip("\n").split(";")

        num_attributes = len(items)

        i = 0
        insert_line = "INSERT INTO routes VALUES ("
        while i < num_attributes:
            item = items[i].replace("'", "''")
            insert_line = insert_line + "'" + item + "'"
            if i != num_attributes - 1:
                insert_line = insert_line + ", "
            i = i + 1

        insert_line = insert_line + ");"
        print(insert_line)
