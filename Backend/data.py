import pandas as pd
import os

# Path to dataset 
DATA_FILE = os.path.join(os.path.dirname(__file__), "creditcard.csv")

def load_data():
    if not os.path.exists(DATA_FILE):
        print("Dataset not found. Please place 'creditcard.csv' in the backend folder.")
        return None
    data = pd.read_csv(DATA_FILE)
    print(f"Dataset loaded successfully! Shape: {data.shape}")
    return data

if __name__ == "__main__":
    df = load_data()
    if df is not None:
        print(df.head())
