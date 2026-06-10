"""Calculate fund-level return and risk metrics from cleaned NAV history."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NAV_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_nav_history.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "derived_fund_metrics.csv"

TRADING_DAYS_PER_YEAR = 252
DEFAULT_RISK_FREE_RATE = 0.065
LOGGER = logging.getLogger(__name__)


def calculate_fund_metrics(
    nav_path: Path = NAV_PATH,
    output_path: Path = OUTPUT_PATH,
    risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
) -> pd.DataFrame:
    """Calculate annualized return, volatility, Sharpe ratio, and drawdown."""
    nav = pd.read_csv(nav_path, parse_dates=["date"])
    nav = nav.sort_values(["amfi_code", "date"]).copy()
    nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()

    records: list[dict[str, object]] = []
    for amfi_code, fund in nav.groupby("amfi_code", sort=True):
        returns = fund["daily_return"].dropna()
        elapsed_days = (fund["date"].iloc[-1] - fund["date"].iloc[0]).days
        elapsed_years = elapsed_days / 365.25
        total_return = fund["nav"].iloc[-1] / fund["nav"].iloc[0] - 1
        annualized_return = (
            (1 + total_return) ** (1 / elapsed_years) - 1
            if elapsed_years > 0
            else np.nan
        )
        annualized_volatility = returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
        sharpe_ratio = (
            (annualized_return - risk_free_rate) / annualized_volatility
            if annualized_volatility > 0
            else np.nan
        )
        drawdown = fund["nav"] / fund["nav"].cummax() - 1

        records.append(
            {
                "amfi_code": amfi_code,
                "observations": len(fund),
                "start_date": fund["date"].iloc[0].date().isoformat(),
                "end_date": fund["date"].iloc[-1].date().isoformat(),
                "total_return_pct": total_return * 100,
                "annualized_return_pct": annualized_return * 100,
                "annualized_volatility_pct": annualized_volatility * 100,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown_pct": drawdown.min() * 100,
            }
        )

    metrics = pd.DataFrame.from_records(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output_path, index=False)
    LOGGER.info("Wrote metrics for %s funds to %s", len(metrics), output_path)
    return metrics


def main() -> None:
    """Calculate and save derived fund metrics."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    calculate_fund_metrics()


if __name__ == "__main__":
    main()
