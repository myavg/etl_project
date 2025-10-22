import time
import psycopg2
import os

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="postgres",
                host="db",
                port="5432"
            )
            conn.close()
            print("Database is ready!")
            break
        except psycopg2.OperationalError:
            time.sleep(3)

if __name__ == "__main__":
    wait_for_db()
