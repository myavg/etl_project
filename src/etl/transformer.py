from sklearn.model_selection import train_test_split
import pandas as pd

class Transformer:
    def transform(self, df: pd.DataFrame) -> tuple:
        X = df.drop("quality", axis=1)
        y = (df["quality"] >= 6).astype(int)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        print("Data transformed and split.")
        return X_train, X_test, y_train, y_test
