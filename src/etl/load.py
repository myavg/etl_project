import psycopg2

def load_to_postgresql(sample, preds):
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
