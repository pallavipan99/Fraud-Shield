import os, json, datetime, math
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from joblib import load

from utils import preprocess_input, expected_features, model_version

DB_URL = os.getenv("DB_URL", "sqlite:///fraudshield.db")

app = Flask(__name__)
CORS(app)

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    amount = Column(Float, default=0.0)
    features = Column(Text)   # JSON blob
    score = Column(Float, default=0.0)
    is_fraud = Column(Integer, default=0)
    model_version = Column(String(64), default="v1")

Base.metadata.create_all(engine)

# Load model artifacts
MODEL_DIR = os.getenv("MODEL_DIR", os.path.join(os.path.dirname(__file__), "models"))
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.joblib")
META_PATH = os.path.join(MODEL_DIR, "meta.json")

_model = None
_scaler = None
_meta = None

def load_artifacts():
    global _model, _scaler, _meta
    try:
        _model = load(MODEL_PATH)
        _scaler = load(SCALER_PATH)
        with open(META_PATH, "r") as f:
            _meta = json.load(f)
        print(f"Loaded model: {_meta.get('model_name')} auroc={_meta.get('auroc'):.4f}")
    except Exception as e:
        print("WARN: Could not load model artifacts. Train first. Error:", e)

load_artifacts()

@app.get("/api/health")
def health():
    return jsonify({"status":"ok", "model_loaded": bool(_model), "model_version": _meta.get("version") if _meta else None})

@app.post("/api/predict")
def predict():
    if _model is None or _scaler is None:
        return jsonify({"error":"Model not loaded. Run training first."}), 500
    payload = request.get_json(force=True, silent=True) or {}
    x, amount, missing = preprocess_input(payload, _scaler, _meta.get("features", expected_features))
    prob = float(_model.predict_proba(x)[0,1]) if hasattr(_model,"predict_proba") else float(_model.decision_function(x)[0])
    flagged = int(prob >= _meta.get("threshold", 0.5))
    return jsonify({"probability": prob, "flagged": flagged, "missing_features": missing, "amount": amount})

@app.post("/api/transactions")
def ingest():
    if _model is None or _scaler is None:
        return jsonify({"error":"Model not loaded. Run training first."}), 500
    payload = request.get_json(force=True, silent=True) or {}
    x, amount, missing = preprocess_input(payload, _scaler, _meta.get("features", expected_features))
    prob = float(_model.predict_proba(x)[0,1]) if hasattr(_model,"predict_proba") else float(_model.decision_function(x)[0])
    flagged = int(prob >= _meta.get("threshold", 0.5))
    # Persist
    with SessionLocal() as db:
        rec = Transaction(amount=float(amount or 0.0), features=json.dumps(payload), score=prob, is_fraud=flagged, model_version=_meta.get("version","v1"))
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return jsonify({"id": rec.id, "ts": rec.ts.isoformat(), "amount": rec.amount, "probability": prob, "flagged": flagged})

@app.get("/api/transactions")
def list_transactions():
    flagged = request.args.get("flagged")
    limit = int(request.args.get("limit", 50))
    with SessionLocal() as db:
        q = db.query(Transaction).order_by(Transaction.ts.desc())
        if flagged in ("1","true","True","yes"):
            q = q.filter(Transaction.is_fraud==1)
        if limit:
            q = q.limit(limit)
        rows = q.all()
        return jsonify([{"id":r.id,"ts":r.ts.isoformat(),"amount":r.amount,"probability":r.score,"flagged":r.is_fraud} for r in rows])

@app.post("/api/batch-score")
def batch_score():
    if _model is None or _scaler is None:
        return jsonify({"error":"Model not loaded. Run training first."}), 500
    payload = request.get_json(force=True, silent=True) or {}
    items = payload if isinstance(payload, list) else payload.get("rows", [])
    res = []
    for row in items:
        x, amount, _ = preprocess_input(row, _scaler, _meta.get("features", expected_features))
        prob = float(_model.predict_proba(x)[0,1]) if hasattr(_model,"predict_proba") else float(_model.decision_function(x)[0])
        flagged = int(prob >= _meta.get("threshold", 0.5))
        res.append({"amount": amount, "probability": prob, "flagged": flagged})
    return jsonify(res)

@app.get("/api/metrics")
def metrics():
    last_minutes = int(request.args.get("last_minutes", 1440))
    since = datetime.datetime.utcnow() - datetime.timedelta(minutes=last_minutes)
    with SessionLocal() as db:
        total = db.query(Transaction).count()
        flagged = db.query(Transaction).filter(Transaction.is_fraud==1).count()
        q = db.query(Transaction).filter(Transaction.ts >= since).order_by(Transaction.ts.asc())
        timeseries = [{"t": r.ts.isoformat(), "flagged": r.is_fraud} for r in q.all()]
    rate = (flagged / total) if total else 0.0
    return jsonify({"total": total, "flagged": flagged, "flagged_rate": rate, "timeseries": timeseries})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5001")), debug=True)
