# backend/save_model.py
import joblib
from backend.train_rf import train_random_forest

def save_model():
    """
    Train the RandomForest classifier and save the model to disk using joblib.
    """
    # Train model
    train_random_forest()  # This trains and saves model & feature importances

    # Optionally, load the model to confirm
    model = joblib.load("backend/random_forest_model.pkl")
    print("Trained model loaded successfully. Ready for predictions.")

if __name__ == "__main__":
    save_model()
