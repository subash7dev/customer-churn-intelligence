from test_prediction import customer
from explainability import explain_prediction


result = explain_prediction(
    customer,
    top_n=10
)

print("\nTop Churn Drivers")
print("------------------")

for _, row in result.iterrows():

    direction = (
        "increases"
        if row["impact"] > 0
        else "decreases"
    )

    print(
        f"{row['feature']}: "
        f"{direction} churn risk "
        f"({row['impact']:.4f})"
    )