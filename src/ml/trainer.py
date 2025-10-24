from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class Trainer:
    def __init__(self, n_estimators=50, random_state=42):
        self.n_estimators = n_estimators
        self.random_state = random_state

    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
        model = RandomForestClassifier(
            n_estimators=self.n_estimators,
            random_state=self.random_state
        )
        model.fit(X_train, y_train)
        print("Model trained.")
        return model
