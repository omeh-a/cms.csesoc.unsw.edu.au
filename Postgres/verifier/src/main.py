from typing import DefaultDict
import psycopg
import sys
import yaml

from colorama import init, Back, Fore, Style
init()

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
def check_column(column, records, table):
    name, data_type = column["name"], column["type"]

    if name not in records.keys():
        raise NameError(f"Column '{name}' does not exist in table '{table}'")

    if records[name] != data_type:
        raise TypeError(f"Expected type '{data_type}' for column {name}, got '{records[name]}'")

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

# Main program
filename = sys.argv[1]

with open(filename) as FILE:
    contents = yaml.load(FILE, Loader=yaml.Loader)

    passed = 0
    total = 0
    errors = DefaultDict(list)

    for table in contents.keys():
        print(f"Scanning through table '{table}': ", end="")

        records = get_columns(cursor, table)
        table_checks = contents[table]
        total += len(table_checks)

        for column in table_checks:
            try:
                check_column(column, records, table)
                passed += 1

                print(f"{Fore.GREEN}.{Style.RESET_ALL}", end="")
            except (TypeError, NameError) as e:
                print(f"{Fore.RED}X{Style.RESET_ALL}", end="")
                errors[table].append(e)

        print("")

    for table, values in errors.items():
        print("")
        print(f"All errors for table '{table}':")

        for error in values:
            print(error)

    print("")

print(f"{passed}/{total} total test cases passed!")
