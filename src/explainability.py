import shap
import pandas as pd

from prediction import model, prepare_customer_features


def explain_prediction(customer, top_n=10):
    """
    Generate SHAP feature contributions for one customer.
    """

    # Prepare features exactly as the prediction pipeline does
    features = prepare_customer_features(customer)

    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)

    # Calculate SHAP values
    shap_values = explainer.shap_values(features)

    # Handle different SHAP versions / output formats
    if isinstance(shap_values, list):
        values = shap_values[1][0]

    elif len(shap_values.shape) == 3:
        values = shap_values[0, :, 1]

    else:
        values = shap_values[0]

    explanation = pd.DataFrame({
        "feature": features.columns,
        "impact": values,
        "absolute_impact": abs(values)
    })

    explanation = (
        explanation
        .sort_values(
            "absolute_impact",
            ascending=False
        )
        .head(top_n)
        .drop(columns=["absolute_impact"])
    )

    return explanation