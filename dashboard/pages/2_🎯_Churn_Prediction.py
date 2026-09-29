import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT / "src")
)

from prediction import predict_churn
from explainability import explain_prediction

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT / "src")
)

from prediction import predict_churn
from explainability import explain_prediction
# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT / "src")
)

from prediction import predict_churn


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🎯 Customer Churn Prediction")

st.markdown(
    """
    Enter customer information to estimate their
    probability of churn and identify their risk level.
    """
)


# --------------------------------------------------
# Customer Profile
# --------------------------------------------------

st.header("Customer Profile")

col1, col2, col3 = st.columns(3)

with col1:

    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        [0, 1],
        format_func=lambda x:
            "Yes" if x == 1 else "No"
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

with col2:

    tenure = st.slider(
        "Tenure (months)",
        min_value=0,
        max_value=72,
        value=12
    )

    phone_service = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        [
            "No",
            "Yes",
            "No phone service"
        ]
    )

    internet_service = st.selectbox(
        "Internet Service",
        [
            "DSL",
            "Fiber optic",
            "No"
        ]
    )

with col3:

    contract = st.selectbox(
        "Contract",
        [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    )

    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )


# --------------------------------------------------
# Services
# --------------------------------------------------

st.header("Services")

service_col1, service_col2, service_col3 = st.columns(3)

with service_col1:

    online_security = st.selectbox(
        "Online Security",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

    online_backup = st.selectbox(
        "Online Backup",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

with service_col2:

    device_protection = st.selectbox(
        "Device Protection",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

    tech_support = st.selectbox(
        "Tech Support",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

with service_col3:

    streaming_tv = st.selectbox(
        "Streaming TV",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        [
            "Yes",
            "No",
            "No internet service"
        ]
    )


# --------------------------------------------------
# Financial information
# --------------------------------------------------

st.header("Financial Information")

finance_col1, finance_col2 = st.columns(2)

with finance_col1:

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        max_value=200.0,
        value=70.0,
        step=1.0
    )

with finance_col2:

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        max_value=10000.0,
        value=monthly_charges * max(tenure, 1),
        step=10.0
    )


# --------------------------------------------------
# Prediction
# --------------------------------------------------

st.divider()

predict_button = st.button(
    "🔮 Predict Churn Risk",
    type="primary",
    use_container_width=True
)


if predict_button:

    customer = {

        "gender": gender,

        "SeniorCitizen": senior_citizen,

        "Partner": 1 if partner == "Yes" else 0,

        "Dependents": 1 if dependents == "Yes" else 0,

        "tenure": tenure,

        "PhoneService": phone_service,

        "MultipleLines": multiple_lines,

        "InternetService": internet_service,

        "OnlineSecurity": online_security,

        "OnlineBackup": online_backup,

        "DeviceProtection": device_protection,

        "TechSupport": tech_support,

        "StreamingTV": streaming_tv,

        "StreamingMovies": streaming_movies,

        "Contract": contract,

        "PaperlessBilling":
            1 if paperless_billing == "Yes" else 0,

        "PaymentMethod": payment_method,

        "MonthlyCharges": monthly_charges,

        "TotalCharges": total_charges
    }

    result = predict_churn(customer)

    

    explanation = explain_prediction(
    customer,
    top_n=8
)

    probability = result["probability"]

    risk = result["risk"]

    prediction = result["prediction"]


    # --------------------------------------------------
    # Result
    # --------------------------------------------------

    st.header("Prediction Result")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:

        st.metric(
            "Churn Probability",
            f"{probability:.2%}"
        )

    with result_col2:

        st.metric(
            "Risk Level",
            risk
        )

    with result_col3:

        st.metric(
            "Prediction",
            "Likely to Churn"
            if prediction == 1
            else "Likely to Stay"
        )


    # --------------------------------------------------
    # Probability bar
    # --------------------------------------------------

    st.progress(
        probability,
        text=f"Churn probability: {probability:.1%}"
    )


    # --------------------------------------------------
    # Business interpretation
    # --------------------------------------------------

    if risk == "High":

        st.error(
            """
            **High Churn Risk**

            This customer shows a high predicted probability
            of churn. Consider proactive retention actions such
            as personalized offers, service improvements,
            contract incentives, or customer outreach.
            """
        )

    elif risk == "Medium":

        st.warning(
            """
            **Medium Churn Risk**

            This customer has a moderate predicted churn risk.
            Consider monitoring engagement and addressing
            potential service or pricing concerns.
            """
        )

    else:

        st.success(
            """
            **Low Churn Risk**

            This customer currently shows a lower predicted
            probability of churn. Continue normal engagement
            and customer experience monitoring.
            """
        )


    # --------------------------------------------------
    # Explainability
    # --------------------------------------------------

    st.header("🔍 Why This Prediction?")

    st.markdown(
        """
        The features below had the strongest influence
        on this customer's churn prediction.
        """
    )

    display_df = explanation.copy()

    display_df["Direction"] = display_df["impact"].apply(
        lambda x:
            "↑ Higher churn risk"
            if x > 0
            else "↓ Lower churn risk"
    )

    display_df["Impact"] = display_df["impact"].abs()

    display_df = display_df[
        [
            "feature",
            "Direction",
            "Impact"
        ]
    ]

    display_df.columns = [
        "Feature",
        "Effect",
        "Impact"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )