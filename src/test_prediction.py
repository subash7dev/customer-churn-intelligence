from prediction import predict_churn


customer = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": 0,
    "Dependents": 0,

    "tenure": 5,

    "PhoneService": "Yes",
    "MultipleLines": "No",

    "InternetService": "Fiber optic",

    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",

    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",

    "Contract": "Month-to-month",

    "PaperlessBilling": 1,

    "PaymentMethod": "Electronic check",

    "MonthlyCharges": 85.50,

    "TotalCharges": 427.50
}


result = predict_churn(customer)

print("\nCustomer Churn Prediction")
print("-------------------------")

print(
    f"Prediction: {result['prediction']}"
)

print(
    f"Churn Probability: "
    f"{result['probability']:.2%}"
)

print(
    f"Risk Level: {result['risk']}"
)