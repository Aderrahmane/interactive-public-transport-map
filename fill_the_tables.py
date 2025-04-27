def insert_line_at_end(file_path, line_to_insert):
    try:
        with open(file_path, 'a') as file:
            file.write(line_to_insert + '\n')
        print(f"Line '{line_to_insert}' inserted at the end of {file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    file_path = "your_file.txt"  # Replace with the path to your file
    line_to_insert = "This is the line to insert"

    insert_line_at_end(file_path, line_to_insert)