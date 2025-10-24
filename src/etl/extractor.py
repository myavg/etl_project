import pandas as pd

class Extractor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path)
        df.columns = df.columns.str.strip().str.lower()
        print(f"Data extracted from {self.file_path}")
        return df
