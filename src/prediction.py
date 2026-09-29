import joblib
import pandas as pd
from pathlib import Path


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "churn_model.pkl"
SCALER_PATH = PROJECT_ROOT / "models" / "scaler.pkl"
FEATURES_PATH = PROJECT_ROOT / "models" / "feature_columns.pkl"


# ============================================================
# Load model artifacts
# ============================================================

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_columns = joblib.load(FEATURES_PATH)


# ============================================================
# Feature preparation
# ============================================================

def prepare_customer_features(customer):

    df = pd.DataFrame([customer])

    # --------------------------------------------------------
    # Convert Yes/No binary fields
    # --------------------------------------------------------

    binary_columns = [
        "Partner",
        "Dependents",
        "PhoneService",
        "PaperlessBilling"
    ]

    for column in binary_columns:

        if column in df.columns:
            df[column] = (
                df[column]
                .replace({
                    "Yes": 1,
                    "No": 0
                })
            )

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).fillna(0).astype(int)

    # --------------------------------------------------------
    # Numerical features
    # --------------------------------------------------------

    df["TenureYears"] = df["tenure"] / 12

    df["IsNewCustomer"] = (
        df["tenure"] <= 12
    ).astype(int)

    df["IsLongTermCustomer"] = (
        df["tenure"] >= 48
    ).astype(int)

    df["EstimatedAnnualCharges"] = (
        df["MonthlyCharges"] * 12
    )

    df["ChargePerTenureMonth"] = (
        df["TotalCharges"] /
        df["tenure"].replace(0, 1)
    )

    # --------------------------------------------------------
    # Service flags
    # --------------------------------------------------------

    service_columns = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]

    for column in service_columns:
        df[f"{column}_Flag"] = (
            df[column] == "Yes"
        ).astype(int)

    df["TotalAdditionalServices"] = sum(
        (df[column] == "Yes").astype(int)
        for column in service_columns
    )

    # --------------------------------------------------------
    # Customer indicators
    # --------------------------------------------------------

    df["HasFamily"] = (
        (df["Partner"] == 1) |
        (df["Dependents"] == 1)
    ).astype(int)

    df["HighMonthlyCharge"] = (
        df["MonthlyCharges"] >= 70
    ).astype(int)

    df["MonthToMonth"] = (
        df["Contract"] == "Month-to-month"
    ).astype(int)

    df["ElectronicCheck"] = (
        df["PaymentMethod"] ==
        "Electronic check"
    ).astype(int)

    # --------------------------------------------------------
    # One-hot encoding
    # --------------------------------------------------------

    categorical_columns = [
        "gender",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaymentMethod"
    ]

    df = pd.get_dummies(
        df,
        columns=categorical_columns,
        drop_first=False
    )

    # --------------------------------------------------------
    # Remove unused columns
    # --------------------------------------------------------

    columns_to_drop = [
        "customerID",
        "Churn"
    ]

    for column in columns_to_drop:
        if column in df.columns:
            df = df.drop(columns=[column])

    # --------------------------------------------------------
    # Align exactly with training feature columns
    # --------------------------------------------------------

    df = df.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # --------------------------------------------------------
    # Force every feature to numeric
    # --------------------------------------------------------

    for column in df.columns:

        if df[column].dtype == bool:
            df[column] = df[column].astype(int)
        else:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).fillna(0)

    # --------------------------------------------------------
    # Scale numerical features
    # --------------------------------------------------------

    numerical_columns = [
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "TenureYears",
        "EstimatedAnnualCharges",
        "ChargePerTenureMonth"
    ]

    existing_numeric = [
        column
        for column in numerical_columns
        if column in df.columns
    ]

    if existing_numeric:
        df[existing_numeric] = scaler.transform(
            df[existing_numeric]
        )

    # Final safety check
    df = df.astype(float)

    return df


# ============================================================
# Prediction
# ============================================================

def predict_churn(customer):

    features = prepare_customer_features(customer)

    probability = model.predict_proba(
        features
    )[0][1]

    prediction = int(
        probability >= 0.5
    )

    if probability <= 0.30:
        risk = "Low"
    elif probability <= 0.60:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "prediction": prediction,
        "probability": float(probability),
        "risk": risk
    }