import psycopg2

class DatabaseManager:
    def __init__(self, host="db", port=5432, user="postgres", password="postgres", dbname="wine_db"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname

    def create_database_and_table(self) -> None:
        conn = psycopg2.connect(
            dbname="postgres",
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (self.dbname,))
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {self.dbname} OWNER {self.user};")
            print(f"Database '{self.dbname}' created.")
        else:
            print(f"Database '{self.dbname}' already exists.")
        cur.close()
        conn.close()

        conn_db = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        cur_db = conn_db.cursor()
        cur_db.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            fixed_acidity FLOAT,
            volatile_acidity FLOAT,
            citric_acid FLOAT,
            residual_sugar FLOAT,
            chlorides FLOAT,
            free_sulfur_dioxide FLOAT,
            total_sulfur_dioxide FLOAT,
            density FLOAT,
            ph FLOAT,
            sulphates FLOAT,
            alcohol FLOAT,
            prediction INT
        );
        """)
        conn_db.commit()
        cur_db.close()
        conn_db.close()
        print("Table 'predictions' is ready.")