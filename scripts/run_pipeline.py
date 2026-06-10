"""Run the Bluestock mutual-fund analytics pipeline from start to finish."""

from __future__ import annotations

import argparse
import logging
import sqlite3

import pandas as pd

from scripts.compute_metrics import calculate_fund_metrics
from scripts.etl_pipeline import DATABASE_PATH, load_datasets
from scripts.live_nav_fetch import download_nav_data
from scripts.recommender import PERFORMANCE_PATH, recommend_funds
from scripts.run_queries import execute_queries
from scripts.run_schema import create_schema

LOGGER = logging.getLogger(__name__)


def validate_database() -> dict[str, int]:
    """Validate SQLite integrity, foreign keys, and loaded table counts."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {integrity}")

        foreign_key_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
        if foreign_key_errors:
            raise RuntimeError(
                f"Foreign-key validation found {len(foreign_key_errors)} errors"
            )

        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()
        return {
            table_name: connection.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            ).fetchone()[0]
            for (table_name,) in tables
        }


def parse_args() -> argparse.Namespace:
    """Parse pipeline command-line options."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fetch-live-nav",
        action="store_true",
        help="Download live NAV files before running local processing.",
    )
    parser.add_argument(
        "--skip-queries",
        action="store_true",
        help="Skip execution checks for the analytical SQL file.",
    )
    parser.add_argument(
        "--recommend",
        metavar="RISK_GRADE",
        help="Print fund recommendations after the pipeline completes.",
    )
    parser.add_argument(
        "--recommend-limit",
        type=int,
        default=3,
        help="Maximum recommendations to print with --recommend.",
    )
    return parser.parse_args()


def run_pipeline(args: argparse.Namespace) -> None:
    """Execute each pipeline stage and fail immediately on invalid output."""
    if args.fetch_live_nav:
        LOGGER.info("Stage 1/5: downloading live NAV history")
        download_nav_data()
    else:
        LOGGER.info("Stage 1/5: live NAV download skipped")

    LOGGER.info("Stage 2/5: calculating derived fund metrics")
    calculate_fund_metrics()

    LOGGER.info("Stage 3/5: rebuilding the SQLite schema")
    create_schema(reset=True)

    LOGGER.info("Stage 4/5: loading processed datasets")
    load_datasets()

    LOGGER.info("Stage 5/5: validating the database")
    row_counts = validate_database()
    LOGGER.info(
        "Validated %s tables containing %s rows",
        len(row_counts),
        sum(row_counts.values()),
    )

    if not args.skip_queries:
        results = execute_queries()
        LOGGER.info("Validated %s analytical SQL queries", len(results))

    if args.recommend:
        funds = pd.read_csv(PERFORMANCE_PATH)
        recommendations = recommend_funds(
            args.recommend,
            funds,
            args.recommend_limit,
        )
        if recommendations.empty:
            raise ValueError(f"No funds match risk grade {args.recommend!r}")
        print("\nRecommendations")
        print(recommendations.to_string(index=False))

    LOGGER.info("Pipeline completed successfully")


def main() -> None:
    """Run the command-line pipeline."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    run_pipeline(parse_args())


if __name__ == "__main__":
    main()
