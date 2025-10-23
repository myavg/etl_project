import psycopg2

def init_db():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""
    SELECT 1 FROM pg_database WHERE datname = 'wine_db';
    """)
    if not cur.fetchone():
        cur.execute("CREATE DATABASE wine_db OWNER postgres;")
        print("Database 'wine_db' created")
    else:
        print("Database already exists")

    cur.close()
    conn.close()

    conn_db = psycopg2.connect(
        dbname="wine_db",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
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
    print("Database initialized successfully.")
