import os, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, classification_report
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
try:
    import xgboost as xgb
    HAS_XGB = True
except Exception:
    HAS_XGB = False

from joblib import dump

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "creditcard.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)

def load_dataset():
    if os.path.exists(DATA_PATH):
        print("Loading dataset from:", DATA_PATH)
        df = pd.read_csv(DATA_PATH)
        # Expect columns: V1..V28, Amount, Class
        feature_cols = [c for c in df.columns if c.startswith("V")] + ["Amount"]
        X = df[feature_cols].values
        y = df["Class"].values
        features = [*feature_cols[:-1], "amount"]  # rename Amount to amount
        # rename Amount to amount
        df_features = pd.DataFrame(X, columns=feature_cols)
        df_features.rename(columns={"Amount":"amount"}, inplace=True)
        return df_features.values, y, [c if c!="Amount" else "amount" for c in feature_cols]
    else:
        print("Dataset not found. Generating synthetic imbalanced dataset...")
        X, y = make_classification(n_samples=30000, n_features=30, n_informative=10, n_redundant=10,
                                   weights=[0.995, 0.005], random_state=42)
        features = [f"f{i}" for i in range(1,31)]
        # append amount as a positive value correlated with y a bit
        rng = np.random.default_rng(42)
        amount = rng.gamma(shape=2.0, scale=50.0, size=X.shape[0]).astype(float)
        X = np.hstack([X, amount.reshape(-1,1)])
        features = features + ["amount"]
        return X, y, features

def train_and_select(X, y, features):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    scaler = StandardScaler().fit(X_train)
    X_train_s = scaler.transform(X_train)
    X_test_s = scaler.transform(X_test)

    # SMOTE on training only
    sm = SMOTE(sampling_strategy=0.1, random_state=42)
    X_train_bal, y_train_bal = sm.fit_resample(X_train_s, y_train)

    candidates = []

    rf = RandomForestClassifier(n_estimators=300, max_depth=None, n_jobs=-1, random_state=42)
    rf.fit(X_train_bal, y_train_bal)
    rf_auc = roc_auc_score(y_test, rf.predict_proba(X_test_s)[:,1])
    candidates.append(("RandomForest", rf, rf_auc))

    mlp = MLPClassifier(hidden_layer_sizes=(64,32), max_iter=30, random_state=42)
    mlp.fit(X_train_bal, y_train_bal)
    mlp_auc = roc_auc_score(y_test, mlp.predict_proba(X_test_s)[:,1])
    candidates.append(("MLP", mlp, mlp_auc))

    if HAS_XGB:
        xgb_model = xgb.XGBClassifier(max_depth=4, n_estimators=400, learning_rate=0.1, subsample=0.9, colsample_bytree=0.9, eval_metric='auc', n_jobs=-1, random_state=42)
        xgb_model.fit(X_train_bal, y_train_bal)
        xgb_auc = roc_auc_score(y_test, xgb_model.predict_proba(X_test_s)[:,1])
        candidates.append(("XGBoost", xgb_model, xgb_auc))

    best = max(candidates, key=lambda t: t[2])
    name, model, auc = best
    print("Selected:", name, "AUROC=", auc)

    # Choose a threshold targeting high recall on fraud class (class=1)
    # You can tune this based on business needs; here we set at 0.5 as default
    threshold = 0.5

    # Persist artifacts
    dump(model, os.path.join(MODEL_DIR, "model.joblib"))
    dump(scaler, os.path.join(MODEL_DIR, "scaler.joblib"))
    meta = {"version":"v1", "model_name":name, "auroc": float(auc), "threshold": threshold, "features": features}
    with open(os.path.join(MODEL_DIR, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Saved model artifacts to", MODEL_DIR)

if __name__ == "__main__":
    X, y, features = load_dataset()
    train_and_select(X, y, features)
