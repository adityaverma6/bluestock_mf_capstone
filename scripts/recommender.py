import pandas as pd
import os

print("Current Working Directory:", os.getcwd())

# Load scheme performance data
funds = pd.read_csv("data/processed/cleaned_scheme_performance.csv")

# Check columns
print(funds.columns)

# Recommendation Function
def recommend_funds(risk_appetite, funds_df):

    recommendations = (
        funds_df[
            funds_df["risk_grade"]
            .str.lower() ==
            risk_appetite.lower()
        ]
        .sort_values(
            "sharpe_ratio",
            ascending=False
        )
        .head(3)
    )

    return recommendations[
        [
            "amfi_code",
            "scheme_name",
            "risk_grade",
            "sharpe_ratio"
        ]
    ]


# User Input
risk_input = input(
    "Enter Risk Appetite (Low/Moderate/High): "
)

recommendations = recommend_funds(
    risk_input,
    funds
)

print("\nRecommended Funds")
print(recommendations)

#Pretty Recommendation Table
recommendations = (
    recommend_funds("Moderate", funds)
)

print(
    recommendations.to_string(index=False)
)
