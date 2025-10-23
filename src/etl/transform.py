from sklearn.model_selection import train_test_split

def transform(df):
    X = df.drop("quality", axis=1)
    y = (df["quality"] >= 6).astype(int)
    return train_test_split(X, y, test_size=0.2, random_state=42)
