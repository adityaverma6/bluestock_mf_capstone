"""Load cleaned mutual-fund datasets into the project SQLite database."""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATABASE_PATH = PROJECT_ROOT / "data" / "db" / "bluestock_mf_pipeline.db"

LOGGER = logging.getLogger(__name__)

DATASETS = {
    "dim_fund": "cleaned_fund_master.csv",
    "fact_nav": "cleaned_nav_history.csv",
    "fact_transactions": "cleaned_investor_transactions.csv",
    "fact_performance": "cleaned_scheme_performance.csv",
    "fact_portfolio_holdings": "cleaned_portfolio_holdings.csv",
    "fact_benchmark_returns": "cleaned_benchmark_indices.csv",
    "fact_sip_inflows": "cleaned_monthly_sip_inflows.csv",
    "fact_category_inflows": "cleaned_category_inflows.csv",
    "fact_aum": "cleaned_aum_by_fund_house.csv",
    "fact_industry_folios": "cleaned_industry_folio_count.csv",
    "fact_derived_metrics": "derived_fund_metrics.csv",
}


def load_datasets(
    database_path: Path = DATABASE_PATH,
    data_dir: Path = PROCESSED_DATA_DIR,
) -> dict[str, int]:
    """Replace table contents with rows from the cleaned CSV datasets."""
    missing_files = [
        filename for filename in DATASETS.values() if not (data_dir / filename).is_file()
    ]
    if missing_files:
        missing = ", ".join(sorted(missing_files))
        raise FileNotFoundError(f"Missing processed datasets: {missing}")

    row_counts: dict[str, int] = {}
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA journal_mode = MEMORY")
        connection.execute("PRAGMA foreign_keys = ON")
        for table_name in reversed(DATASETS):
            connection.execute(f'DELETE FROM "{table_name}"')
        for table_name, filename in DATASETS.items():
            dataframe = pd.read_csv(data_dir / filename)
            dataframe.to_sql(table_name, connection, if_exists="append", index=False)
            row_counts[table_name] = len(dataframe)
            LOGGER.info("Loaded %s rows into %s", len(dataframe), table_name)

    return row_counts


def main() -> None:
    """Load all processed datasets into SQLite."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    load_datasets()


if __name__ == "__main__":
    main()
