from etl.db_init import init_db
from etl.extract import extract
from etl.transform import transform
from etl.load import load_to_postgresql
from ml.train import train_model

def main():
    init_db()
    df = extract("data/raw/winequality-red.csv")
    X_train, X_test, y_train, y_test = transform(df)
    model = train_model(X_train, y_train)
    sample = X_test.iloc[:5]
    preds = model.predict(sample)
    load_to_postgresql(sample, preds)

if __name__ == "__main__":
    main()
