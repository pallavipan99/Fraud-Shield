import json, os
from joblib import load
import boto3

s3 = boto3.client('s3')
MODEL_BUCKET = os.environ.get('MODEL_BUCKET')
MODEL_KEY = os.environ.get('MODEL_KEY','model.joblib')
SCALER_KEY = os.environ.get('SCALER_KEY','scaler.joblib')

_model = None
_scaler = None

def load_artifacts(tmp='/tmp'):
    global _model, _scaler
    if _model is not None: return
    s3.download_file(MODEL_BUCKET, MODEL_KEY, f"{tmp}/model.joblib")
    s3.download_file(MODEL_BUCKET, SCALER_KEY, f"{tmp}/scaler.joblib")
    _model = load(f"{tmp}/model.joblib")
    _scaler = load(f"{tmp}/scaler.joblib")

def handler(event, context):
    load_artifacts()
    body = event.get('body')
    if isinstance(body, str):
        try: body = json.loads(body)
        except: body = {}
    features = body or {}
    # naive preprocessing: assume already ordered vector
    import numpy as np
    x = np.array([features.get(f"f{i}",0.0) for i in range(1,31)] + [features.get("amount",0.0)], dtype=float).reshape(1,-1)
    xs = _scaler.transform(x)
    prob = float(_model.predict_proba(xs)[0,1]) if hasattr(_model,'predict_proba') else float(_model.decision_function(xs)[0])
    return {"statusCode": 200, "headers": {"Content-Type":"application/json"}, "body": json.dumps({"probability": prob, "flagged": prob>=0.5})}
