import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

def train_xgboost(path="data/creditcard.csv", model_path="backend/xgboost_model.pkl"):
    # Load dataset
    df = pd.read_csv(path)
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Preprocessing
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Handle imbalance with SMOTE
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_scaled, y)

    # Train XGBoost classifier
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    )
    model.fit(X_res, y_res)

    # Save model
    joblib.dump(model, model_path)
    print(f"XGBoost model saved to {model_path}")
    return model

