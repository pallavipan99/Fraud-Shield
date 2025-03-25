from kafka import KafkaConsumer
import json
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler

import os


# Load models
try:
    rf_model = joblib.load("backend/random_forest_model.pkl")
    print("RandomForest loaded")
except:
    rf_model = None
try:
    xgb_model = joblib.load("backend/xgboost_model.pkl")
    print("XGBoost loaded")
except:
    xgb_model = None
try:
    nn_model = load_model("backend/nn_model.h5")
    scaler = joblib.load("backend/scaler.pkl")
    print("Neural Network loaded")
except:
    nn_model = None

# Configure Kafka consumer
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Listening for incoming transactions...")

for message in consumer:
    transaction = message.value
    df = pd.DataFrame([transaction])

    # Preprocess if NN is used
    if nn_model:
        df_scaled = scaler.transform(df)
        nn_pred = nn_model.predict(df_scaled).flatten()[0]
    else:
        nn_pred = None

    # RandomForest prediction
    rf_pred = rf_model.predict(df)[0] if rf_model else None
    # XGBoost prediction
    xgb_pred = xgb_model.predict(df)[0] if xgb_model else None

    print("Transaction:", transaction)
    print(f"Predictions → RF: {rf_pred}, XGB: {xgb_pred}, NN: {nn_pred}")
