# Database

Contains SQLite analytics databases:

- `bluestock_mf.db` is the legacy dashboard database.
- `bluestock_mf_pipeline.db` is rebuilt by `python run_pipeline.py`.

Pipeline tables are defined in `sql/schema.sql`, so the pipeline database
should be treated as generated output.
