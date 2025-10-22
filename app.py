import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
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
    SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'postgres';
    """)
    user_exists = cur.fetchone()
    if not user_exists:
        cur.execute("CREATE ROLE postgres LOGIN PASSWORD 'postgres';")
        print("User created")
    else:
        print("User already exists")

    cur.execute("""
    SELECT 1 FROM pg_database WHERE datname = 'wine_db';
    """)
    db_exists = cur.fetchone()
    if not db_exists:
        cur.execute("CREATE DATABASE wine_db OWNER postgres;")
        print("'wine_db' already created")
    else:
        print("'wine_db' already exists")

    conn.commit()
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
    print("Database, user, and table are ready!")

def extract() -> pd.DataFrame:
    # === Extract ===
    df = pd.read_csv("winequality-red.csv", sep=",")
    df.columns = df.columns.str.strip().str.lower()
    return df

def transform(df: pd.DataFrame) -> tuple:
    # === Transform ===
    X = df.drop("quality", axis=1)
    y = (df["quality"] >= 6).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    # === Train model ===
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    return model

def load_to_postgresql(sample: pd.DataFrame, preds: list) -> None:
    # === Load в PostgreSQL ===
    conn = psycopg2.connect(
        dbname="wine_db",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )

    cur = conn.cursor()

    for i, row in sample.iterrows():
        values = [float(x) for x in row.values]
        prediction = int(preds[list(sample.index).index(i)])
        cur.execute("""
            INSERT INTO predictions (
                fixed_acidity, volatile_acidity, citric_acid,
                residual_sugar, chlorides, free_sulfur_dioxide,
                total_sulfur_dioxide, density, ph, sulphates,
                alcohol, prediction
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, values + [prediction])

    conn.commit()
    cur.close()
    conn.close()

    print("Predictions saved to PostgreSQL!")

if __name__ == "__main__":
    init_db()

    df = extract()
    X_train, X_test, y_train, y_test = transform(df)

    model = train_model(X_train, y_train)
    sample = X_test.iloc[:5]

    preds = model.predict(sample)
    load_to_postgresql(sample, preds)