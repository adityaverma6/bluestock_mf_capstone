# Data

Project data is separated by processing stage:

- `raw/` contains source extracts.
- `processed/` contains cleaned and derived datasets.
- `db/` contains the pipeline-generated SQLite database.

The default pipeline reads processed CSVs and rebuilds the database.
