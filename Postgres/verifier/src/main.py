import psycopg
import sys
import yaml

# TODO: use Docker instead
USERNAME = "postgres"
PASSWORD = "test"
DB = "cms_testing_db"
HOST = "localhost"
PORT = 1234

# Fetch all the columns (name and data type) of a given table.
def get_columns(cursor, table):
    cursor.execute(f"""
        SELECT column_name, udt_name
        FROM information_schema.columns
        WHERE table_name = '{table}'
    """)

    records = {}

    for name, data_type in cursor:
        records[name] = data_type

    return records

# Given a column specified in a YAML file, check if it matches with our
# existing records.
def check_column(column, records):
    name, data_type = column["name"], column["type"]

    if records[name] != data_type:
        raise TypeError(f"Expected type {data_type} for table {name}, got {records[name]}")

# Try connecting to the database
try:
    conn = psycopg.connect(f"""
    dbname={DB}
    user={USERNAME}
    password={PASSWORD}
    host={HOST}
    port={PORT}
    """)

    cursor = conn.cursor()
except (Exception, psycopg.Error) as e:
    raise e

filename = sys.argv[1]

with open(filename) as FILE:
    contents = yaml.load(FILE, Loader=yaml.Loader)
    passed = 0
    total = 0

    for table in contents.keys():
        print(f"Scanning through table '{table}': ", end="")

        records = get_columns(cursor, table)
        existing = contents[table]

        for column in existing:
            try:
                check_column(column, records)
                passed += 1
                
                print(".", end="")
            except TypeError as e:
                print("")
                print(e)

            total += 1

        print("")

print(f"{passed}/{total} total test cases passed!")
