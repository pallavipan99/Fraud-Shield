import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_preprocess(path="backend/creditcard.csv"):
    """
    Load the Kaggle credit card fraud dataset and preprocess features.
    
    Returns:
        X_scaled: Scaled feature matrix
        y: Target labels
    """
    df = pd.read_csv(path)
    X = df.drop("Class", axis=1)
    y = df["Class"]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

if __name__ == "__main__":
    X_scaled, y = load_and_preprocess()
    print(f"Features shape: {X_scaled.shape}, Labels shape: {y.shape}")
