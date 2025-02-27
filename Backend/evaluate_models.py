import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier
from tensorflow.keras.models import load_model
from backend.nn_model import train_nn
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("data/creditcard.csv")
X = df.drop("Class", axis=1)
y = df["Class"]

# Preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Handle imbalance
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X_scaled, y)

# --- RandomForest ---
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_res, y_res)
rf_preds = rf_model.predict_proba(X_res)[:, 1]
rf_auc = roc_auc_score(y_res, rf_preds)
print(f"RandomForest AUC: {rf_auc:.4f}")

# --- XGBoost ---
xgb_model = XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb_model.fit(X_res, y_res)
xgb_preds = xgb_model.predict_proba(X_res)[:, 1]
xgb_auc = roc_auc_score(y_res, xgb_preds)
print(f"XGBoost AUC: {xgb_auc:.4f}")

# --- Neural Network ---
nn_model_path = "backend/nn_model.h5"
scaler_path = "backend/scaler.pkl"
nn_model = load_model(nn_model_path)
scaler = joblib.load(scaler_path)
X_nn_scaled = scaler.transform(X)
nn_preds = nn_model.predict(X_nn_scaled).flatten()
nn_auc = roc_auc_score(y, nn_preds)
print(f"Neural Network AUC: {nn_auc:.4f}")
