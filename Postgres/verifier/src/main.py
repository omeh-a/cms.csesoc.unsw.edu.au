import psycopg
import sys
import yaml

USERNAME = "postgres"
PASSWORD = "test"
DB = "cms_testing_db"
HOST = "localhost"
PORT = 1234

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
    print(e)

filename = sys.argv[1]

with open(filename) as FILE:
    contents = yaml.load(FILE, Loader=yaml.Loader)

    for table in contents.keys():
        records = get_columns(cursor, table)
        existing = contents[table]

        for column in existing:
            name, data_type = column["name"], column["type"]

            if records[name] != data_type:
                raise TypeError(f"Expected type {data_type} for table {name}, got {records[name]}")

print("Success!")
