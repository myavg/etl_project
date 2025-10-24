import time
import psycopg2

def wait_for_db() -> None:
    while True:
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="postgres",
                host="db",
                port="5432"
            )
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM pg_database WHERE datname = 'wine_db';")
            exists = cur.fetchone()
            if not exists:
                cur.execute("CREATE DATABASE wine_db OWNER postgres;")
                print("Database 'wine_db' created!")
            else:
                print("Database 'wine_db' already exists.")
            cur.close()
            conn.close()
            break
        except psycopg2.OperationalError:
            print("Waiting for PostgreSQL to start...")
            time.sleep(3)

if __name__ == "__main__":
    wait_for_db()
