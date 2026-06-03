import sqlite3
import os

# =========================================
# PROJECT ROOT DIRECTORY
# =========================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# =========================================
# PATHS
# =========================================

db_path = os.path.join(
    BASE_DIR,
    "data",
    "db",
    "bluestock_mf.db"
)

query_path = os.path.join(
    BASE_DIR,
    "sql",
    "queries.sql"
)

# =========================================
# CONNECT TO DATABASE
# =========================================

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

# =========================================
# READ SQL FILE
# =========================================

with open(query_path, "r") as f:
    sql_script = f.read()

# =========================================
# SPLIT MULTIPLE QUERIES
# =========================================

queries = sql_script.split(";")

# =========================================
# EXECUTE EACH QUERY
# =========================================

for query in queries:

    query = query.strip()

    if query:

        print("\n" + "=" * 60)

        try:
            cursor.execute(query)

            results = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]

            print(" | ".join(columns))

            print("-" * 60)

            for row in results:
                print(row)

        except Exception as e:
            print(f"Error: {e}")

# =========================================
# CLOSE CONNECTION
# =========================================

conn.close()