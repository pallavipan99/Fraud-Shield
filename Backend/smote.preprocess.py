# backend/smote_preprocess.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def load_preprocess_smote(path="backend/creditcard.csv"):
    """
    Load dataset, scale features, and apply SMOTE to handle class imbalance.
    
    Returns:
        X_resampled: Resampled feature matrix
        y_resampled: Resampled target labels
    """
    df = pd.read_csv(path)
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Apply SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_scaled, y)
    
    return X_resampled, y_resampled

if __name__ == "__main__":
    X_res, y_res = load_preprocess_smote()
    print(f"Resampled features shape: {X_res.shape}, Resampled labels shape: {y_res.shape}")
