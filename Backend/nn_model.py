import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

def train_nn(path="data/creditcard.csv", model_path="backend/nn_model.h5", scaler_path="backend/scaler.pkl"):
    # Load dataset
    df = pd.read_csv(path)
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Preprocessing
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, scaler_path)

    # Handle imbalance with SMOTE
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_scaled, y)

    # Build simple NN
    model = Sequential([
        Dense(32, input_dim=X_res.shape[1], activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train
    es = EarlyStopping(monitor='loss', patience=3, restore_best_weights=True)
    model.fit(X_res, y_res, epochs=20, batch_size=32, callbacks=[es], verbose=1)

    # Save model
    model.save(model_path)
    print(f"Neural Network model saved to {model_path}")
    return model, scaler
