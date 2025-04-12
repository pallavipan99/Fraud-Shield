
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


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


app = Flask(__name__)

# Configure JWT
app.config["JWT_SECRET_KEY"] = "supersecretkey"  # Change to a secure key in production
jwt = JWTManager(app)

# Example user login endpoint
@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    # Example authentication
    if username == "admin" and password == "password":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad credentials"}), 401

# Protect endpoints
@app.route("/api/predict", methods=["POST"])
@jwt_required()
def predict():
    # Your existing predict code here
    return jsonify({"prediction": "dummy"})

@app.route("/api/stream-fraud", methods=["GET"])
@jwt_required()
def stream_fraud():
    # Return last 10 flagged transactions
    return jsonify(flagged_transactions[-10:])