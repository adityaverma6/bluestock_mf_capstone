# Scripts

Reusable command-line stages for the analytics pipeline.

| Script | Purpose |
| --- | --- |
| `compute_metrics.py` | Derives return, volatility, Sharpe, and drawdown metrics |
| `run_schema.py` | Creates or resets the SQLite schema |
| `etl_pipeline.py` | Loads all cleaned CSV datasets into SQLite |
| `run_queries.py` | Executes the analytical SQL statements |
| `recommender.py` | Ranks funds within a selected risk grade |
| `live_nav_fetch.py` | Downloads optional live NAV history from MF API |

Use `python run_pipeline.py` from the repository root for the standard workflow.
