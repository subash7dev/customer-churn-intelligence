import joblib
import pandas as pd

MODEL_PATH = "models/churn_model.pkl"
SCALER_PATH = "models/scaler.pkl"
FEATURES_PATH = "models/feature_columns.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_columns = joblib.load(FEATURES_PATH)

print("Model loaded:", type(model).__name__)
print("Scaler loaded:", type(scaler).__name__)
print("Feature count:", len(feature_columns))

print("\nFirst 20 features:")
for feature in feature_columns[:20]:
    print("-", feature)

print("\nModel test successful.")