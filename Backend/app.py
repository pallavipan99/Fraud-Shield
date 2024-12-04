from flask import Flask, jsonify, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
MODEL_PATH = "backend/random_forest_model.pkl"
model = joblib.load(MODEL_PATH)

@app.route("/")
def home():
    return jsonify({"message": "Fraud Shield Backend is running!"})

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"status": "success", "message": "pong"}), 200

# ✅ Enhanced /predict endpoint
@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Accepts JSON input:
    {
        "features": [[v1, v2, ..., vN], [v1, v2, ..., vN], ...]
    }
    Returns predictions and probabilities for multiple transactions.
    """
    data = request.get_json()
    features = data.get("features")
    
    if not features:
        return jsonify({"error": "No features provided"}), 400

    try:
        df = pd.DataFrame(features)
        preds = model.predict(df)
        probs = model.predict_proba(df).tolist()
        response = [{"prediction": int(p), "probabilities": prob} for p, prob in zip(preds, probs)]
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
