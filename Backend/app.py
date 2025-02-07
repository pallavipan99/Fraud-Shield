@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Accepts JSON input:
    {
        "features": [[v1, v2, ..., vN], ...]
    }
    Returns predictions and probabilities.
    """
    data = request.get_json()
    features = data.get("features")
    
    if not features:
        return jsonify({"error": "No features provided. Please send a 'features' key with a list of feature arrays."}), 400

    try:
        df = pd.DataFrame(features)
        preds = model.predict(df)
        probs = model.predict_proba(df).tolist()
        response = [{"prediction": int(p), "probabilities": prob} for p, prob in zip(preds, probs)]
        return jsonify(response)
    except ValueError as ve:
        return jsonify({"error": f"ValueError: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Load RandomForest model as before
# model = joblib.load("backend/random_forest_model.pkl")
try:
    xgb_model_path = "backend/xgboost_model.pkl"
    xgb_model = joblib.load(xgb_model_path)
    model = xgb_model
    print("Using XGBoost model")
except FileNotFoundError:
    print("XGBoost model not found. Using RandomForest")

