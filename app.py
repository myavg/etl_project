import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import psycopg2

# === Extract ===
df = pd.read_csv("winequality-red.csv", sep=",")
# приведение названий колонок к нижнему регистру без пробелов
df.columns = df.columns.str.strip().str.lower()

# === Transform ===
X = df.drop("quality", axis=1)
y = (df["quality"] >= 6).astype(int)  # бинаризация: хорошее/плохое вино
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# === Train model ===
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# Берём несколько тестовых наблюдений
sample = X_test.iloc[:5]
preds = model.predict(sample)

# === Load в PostgreSQL ===
conn = psycopg2.connect(
    dbname="wine_db",
    user="postgres",
    password="postgres",
    host="db",  # имя сервиса в docker-compose
    port="5432"
)
cur = conn.cursor()

cur.execute("""
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

for i, row in sample.iterrows():
    values = [float(x) for x in row.values]   # преобразуем np.float64 → float
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

print("✅ Predictions saved to PostgreSQL!")
