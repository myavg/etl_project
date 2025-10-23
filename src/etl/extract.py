import pandas as pd

def extract(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()
    return df
