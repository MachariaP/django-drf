#!/usr/bin/env python
import time
import os
from urllib.parse import urlparse
import psycopg2

def wait_for_db():
    url = os.getenv('DATABASE_URL', 'postgres://postgres:postgres@db:5432/postgres')
    parsed = urlparse(url)
    dbname = parsed.path[1:]
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port or 5432

    print(f"Waiting for PostgreSQL at {host}:{port}...")
    while True:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port,
                connect_timeout=3
            )
            conn.close()
            print("PostgreSQL is ready!")
            break
        except Exception as e:
            print("PostgreSQL not ready, retrying in 2s...")
            time.sleep(2)

if __name__ == "__main__":
    wait_for_db()
