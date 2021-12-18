import psycopg
import sys
import yaml

USERNAME = "postgres"
PASSWORD = "test"
DB = "cms_testing_db"
HOST = "localhost"
PORT = 1234

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
        cursor.execute(f"""
        SELECT column_name, udt_name
        FROM information_schema.columns
        WHERE table_name = '{table}'
        """)

        for record in cursor:
            print(record)
