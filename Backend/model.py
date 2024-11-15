# backend/train_rf.py
import joblib
from sklearn.ensemble import RandomForestClassifier
from backend.smote_preprocess import load_preprocess_smote
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

def train_random_forest():
    # Load resampled dataset
    X, y = load_preprocess_smote()

    # Split into train/test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train baseline RandomForest
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save model
    joblib.dump(clf, "backend/random_forest_model.pkl")
    print("Model saved as random_forest_model.pkl")

    # Save feature importances
    feature_importances = pd.DataFrame({
        "feature": [f"V{i}" for i in range(1, X.shape[1]+1)],
        "importance": clf.feature_importances_
    }).sort_values(by="importance", ascending=False)
    feature_importances.to_csv("backend/feature_importances.csv", index=False)
    print("Feature importances saved as feature_importances.csv")

if __name__ == "__main__":
    train_random_forest()
