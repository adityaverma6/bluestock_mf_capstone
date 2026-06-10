"""Create the SQLite schema used by the mutual-fund analytics pipeline."""

from __future__ import annotations

import argparse
import logging
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"
DATABASE_PATH = PROJECT_ROOT / "data" / "db" / "bluestock_mf_pipeline.db"

LOGGER = logging.getLogger(__name__)


def create_schema(
    database_path: Path = DATABASE_PATH,
    schema_path: Path = SCHEMA_PATH,
    reset: bool = False,
) -> None:
    """Create database tables, optionally removing existing pipeline tables."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    schema_sql = schema_path.read_text(encoding="utf-8")

    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA journal_mode = MEMORY")
        if reset:
            connection.execute("PRAGMA foreign_keys = OFF")
            table_names = connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
                """
            ).fetchall()
            for (table_name,) in table_names:
                connection.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        connection.executescript(schema_sql)
        connection.execute("PRAGMA foreign_keys = ON")

    LOGGER.info("Database schema ready at %s", database_path)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop existing application tables before creating the schema.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the schema creation command."""
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    create_schema(reset=args.reset)


if __name__ == "__main__":
    main()
