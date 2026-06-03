import pandas as pd
from sqlalchemy import create_engine
import os

# =========================================
# PROJECT ROOT DIRECTORY
# =========================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# =========================================
# DATABASE PATH
# =========================================

db_path = os.path.join(
    BASE_DIR,
    "data",
    "db",
    "bluestock_mf.db"
)

engine = create_engine(f"sqlite:///{db_path}")

# =========================================
# DATA DIRECTORY
# =========================================

DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

# =========================================
# LOAD CSV FILES
# =========================================

df_fund_master = pd.read_csv(
    os.path.join(DATA_DIR, "cleaned_fund_master.csv")
)

df_nav = pd.read_csv(
    os.path.join(DATA_DIR, "cleaned_nav_history.csv")
)

df_transactions = pd.read_csv(
    os.path.join(DATA_DIR, "cleaned_investor_transactions.csv")
)

df_performance = pd.read_csv(
    os.path.join(DATA_DIR, "cleaned_scheme_performance.csv")
)

df_holdings = pd.read_csv(
    os.path.join(DATA_DIR, "cleaned_portfolio_holdings.csv")
)

# =========================================
# LOAD DATA INTO SQLITE
# =========================================

df_fund_master.to_sql(
    "dim_fund",
    engine,
    if_exists="replace",
    index=False
)

df_nav.to_sql(
    "fact_nav",
    engine,
    if_exists="replace",
    index=False
)

df_transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="replace",
    index=False
)

df_performance.to_sql(
    "fact_performance",
    engine,
    if_exists="replace",
    index=False
)

df_holdings.to_sql(
    "fact_portfolio_holdings",
    engine,
    if_exists="replace",
    index=False
)

print("All datasets loaded successfully!")