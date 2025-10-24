import psycopg2

class Loader:
    def __init__(self, dbname="wine_db", user="postgres", password="postgres", host="db", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def load_predictions(self, sample, preds) -> None:
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
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
        print("Predictions saved to PostgreSQL.")
