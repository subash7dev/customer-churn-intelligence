import streamlit as st


st.set_page_config(
    page_title="Customer Churn Intelligence",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📊 Customer Churn Intelligence")

st.markdown(
    """
    ### AI-powered customer retention analytics

    Analyze customer behavior, identify churn patterns,
    predict individual churn risk, and understand the
    factors driving each prediction.
    """
)


# --------------------------------------------------
# Project overview
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Analytics",
        "PostgreSQL + SQL"
    )

with col2:
    st.metric(
        "Machine Learning",
        "Random Forest"
    )

with col3:
    st.metric(
        "Explainability",
        "SHAP"
    )


st.divider()


# --------------------------------------------------
# Navigation
# --------------------------------------------------

st.subheader("Explore the platform")

st.markdown(
    """
    Use the navigation menu on the left:

    **📊 Analytics**
    - Customer churn KPIs
    - Contract analysis
    - Internet service analysis
    - Payment method analysis
    - Revenue analysis

    **🎯 Churn Prediction**
    - Enter customer information
    - Predict churn probability
    - Risk classification
    - SHAP-based explanation

    **🤖 Model Performance**
    - Model comparison
    - ROC-AUC
    - Precision
    - Recall
    - F1-score
    """
)


st.info(
    "💡 This platform combines data analytics, "
    "machine learning, and explainable AI."
)