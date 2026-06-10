"""Execute the analytical SQL statements against the project database."""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "data" / "db" / "bluestock_mf_pipeline.db"
QUERY_PATH = PROJECT_ROOT / "sql" / "queries.sql"
LOGGER = logging.getLogger(__name__)


def split_queries(sql_script: str) -> list[str]:
    """Split the project's simple semicolon-delimited SQL statements."""
    return [statement.strip() for statement in sql_script.split(";") if statement.strip()]


def execute_queries(
    database_path: Path = DATABASE_PATH,
    query_path: Path = QUERY_PATH,
) -> list[tuple[list[str], list[tuple[object, ...]]]]:
    """Execute all configured queries and return columns with result rows."""
    statements = split_queries(query_path.read_text(encoding="utf-8"))
    query_results: list[tuple[list[str], list[tuple[object, ...]]]] = []

    with sqlite3.connect(database_path) as connection:
        for statement in statements:
            cursor = connection.execute(statement)
            columns = [description[0] for description in cursor.description or []]
            query_results.append((columns, cursor.fetchall()))

    LOGGER.info("Executed %s analytical queries", len(query_results))
    return query_results


def main() -> None:
    """Execute queries and print compact result tables."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for index, (columns, rows) in enumerate(execute_queries(), start=1):
        print(f"\nQuery {index}")
        print(" | ".join(columns))
        for row in rows:
            print(" | ".join(str(value) for value in row))


if __name__ == "__main__":
    main()
