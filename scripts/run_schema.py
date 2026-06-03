import sqlite3
import os

# =========================================
# PROJECT ROOT DIRECTORY
# =========================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# =========================================
# PATHS
# =========================================

schema_path = os.path.join(
    BASE_DIR,
    "sql",
    "schema.sql"
)

db_path = os.path.join(
    BASE_DIR,
    "data",
    "db",
    "bluestock_mf.db"
)

# =========================================
# CREATE DB FOLDER IF NOT EXISTS
# =========================================

os.makedirs(
    os.path.join(BASE_DIR, "data", "db"),
    exist_ok=True
)

# =========================================
# CONNECT TO SQLITE
# =========================================

conn = sqlite3.connect(db_path)

# =========================================
# READ schema.sql
# =========================================

with open(schema_path, "r") as f:
    sql_script = f.read()

# =========================================
# EXECUTE SQL SCRIPT
# =========================================

conn.executescript(sql_script)

print("Schema created successfully!")

conn.close()