import os
import psycopg

USERNAME = os.environ["POSTGRES_USER"]
PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB = os.environ["POSTGRES_DB"]

with psycopg.connect(f"dbname={DB} user={USERNAME} password={PASSWORD}") as conn:
    with conn.cursor() as cur:
        pass
