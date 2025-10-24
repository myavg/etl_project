from src.etl import DatabaseManager, Extractor, Transformer, Loader
from src.ml import Trainer


class Worker:
    def __init__(
        self,
        data_path: str = "data/raw/winequality-red.csv",
        db_host: str = "db",
        db_port: int = 5432,
        db_name: str = "wine_db",
        db_user: str = "postgres",
        db_password: str = "postgres",
    ):
        self.data_path = data_path
        self.db_config = {
            "host": db_host,
            "port": db_port,
            "dbname": db_name,
            "user": db_user,
            "password": db_password,
        }

        self.db = DatabaseManager(**self.db_config)
        self.extractor = Extractor(self.data_path)
        self.transformer = Transformer()
        self.trainer = Trainer()
        self.loader = Loader(**self.db_config)

    def run(self) -> None:
        self.db.create_database_and_table()

        df = self.extractor.extract()

        X_train, X_test, y_train, y_test = self.transformer.transform(df)

        model = self.trainer.train(X_train, y_train)

        sample = X_test.iloc[:5]
        preds = model.predict(sample)
        self.loader.load_predictions(sample, preds)

        print("Pipeline finished successfully!")