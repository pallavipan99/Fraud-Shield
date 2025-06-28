import numpy as np
import json

# default expected features (if meta not available)
expected_features = [f"f{i}" for i in range(1,31)] + ["amount"]
model_version = "v1"

def _get_alt_keys(key: str):
    """Return alternative key names that might appear in payloads.
    - V1..V28 <-> f1..f28
    - Amount/amount interchangeable
    """
    alts = []
    k = key.strip()
    if k.lower().startswith('v') and k[1:].isdigit():
        alts.append('f' + k[1:])  # V1 -> f1
    if k.lower().startswith('f') and k[1:].isdigit():
        alts.append('V' + k[1:])  # f1 -> V1
    if k == 'Amount':
        alts.append('amount')
    if k == 'amount':
        alts.append('Amount')
    return alts

def preprocess_input(payload, scaler, features):
    """Map input JSON to model features.
    Accepts Kaggle-style keys (V1..V28, Amount) or synthetic keys (f1..f30, amount).
    """
    row = []
    missing = []
    amount_val = None
    for f in features:
        val = payload.get(f, None)
        if val is None:
            # try alternates
            for alt in _get_alt_keys(f):
                if alt in payload:
                    val = payload[alt]
                    break
        if f in ('Amount', 'amount'):
            try:
                amount_val = float(val) if val is not None else 0.0
            except Exception:
                amount_val = 0.0
        if val is None:
            missing.append(f)
            val = 0.0
        try:
            row.append(float(val))
        except Exception:
            row.append(0.0)
    X = np.array(row, dtype=float).reshape(1, -1)
    Xs = scaler.transform(X)
    return Xs, amount_val, missing
