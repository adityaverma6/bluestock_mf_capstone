"""Recommend mutual funds for a requested risk grade."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PERFORMANCE_PATH = (
    PROJECT_ROOT / "data" / "processed" / "cleaned_scheme_performance.csv"
)
OUTPUT_COLUMNS = ["amfi_code", "scheme_name", "risk_grade", "sharpe_ratio"]


def recommend_funds(
    risk_appetite: str,
    funds: pd.DataFrame,
    limit: int = 3,
) -> pd.DataFrame:
    """Return the highest-Sharpe funds matching a risk grade."""
    normalized_risk = risk_appetite.strip().casefold()
    recommendations = funds[
        funds["risk_grade"].fillna("").str.casefold() == normalized_risk
    ]
    return (
        recommendations.sort_values("sharpe_ratio", ascending=False)
        .head(limit)
        .loc[:, OUTPUT_COLUMNS]
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("risk_appetite", help="Risk grade, such as Low or Moderate.")
    parser.add_argument("--limit", type=int, default=3, help="Number of funds to return.")
    return parser.parse_args()


def main() -> None:
    """Print fund recommendations for the selected risk grade."""
    args = parse_args()
    funds = pd.read_csv(PERFORMANCE_PATH)
    recommendations = recommend_funds(args.risk_appetite, funds, args.limit)

    if recommendations.empty:
        available = ", ".join(sorted(funds["risk_grade"].dropna().unique()))
        raise SystemExit(f"No matching funds. Available risk grades: {available}")

    print(recommendations.to_string(index=False))


if __name__ == "__main__":
    main()
