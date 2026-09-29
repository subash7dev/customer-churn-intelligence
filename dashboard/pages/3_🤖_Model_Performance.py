import sys
from pathlib import Path

import streamlit as st
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

st.set_page_config(
    page_title="Model Performance",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Model Performance")

st.markdown(
    """
    Evaluate the machine-learning models used for
    customer churn prediction.
    """
)

results_path = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "model_comparison.csv"
)

if not results_path.exists():

    st.warning(
        "Model comparison results were not found."
    )

    st.info(
        "Run notebook 04_model_training.ipynb first."
    )

else:

    results = pd.read_csv(results_path)

    st.subheader("Model Comparison")

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Performance Metrics")

    metric_columns = [
        column
        for column in [
            "Accuracy",
            "Precision",
            "Recall",
            "F1",
            "ROC-AUC"
        ]
        if column in results.columns
    ]

    if metric_columns:

        chart_data = results.set_index(
            results.columns[0]
        )[metric_columns]

        st.bar_chart(chart_data)

    st.divider()

    st.subheader("Production Model")

    st.info(
        """
        The production prediction pipeline uses the
        saved Random Forest model together with the
        trained preprocessing artifacts.
        """
    )