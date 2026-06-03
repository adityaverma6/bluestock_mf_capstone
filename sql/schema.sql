

PRAGMA foreign_keys = ON;

-- =========================================
-- 1. DIMENSION TABLE: FUND MASTER
-- =========================================
CREATE TABLE dim_fund (
    amfi_code TEXT PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    benchmark TEXT,
    launch_date DATE,
    risk_level TEXT,
    expense_ratio REAL,
    fund_manager TEXT,
    fund_type TEXT
);

-- =========================================
-- 2. FACT TABLE: NAV HISTORY
-- =========================================
CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT NOT NULL,
    nav_date DATE NOT NULL,
    nav REAL NOT NULL,
    daily_return REAL,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
        ON DELETE CASCADE
);

-- =========================================
-- 3. FACT TABLE: INVESTOR TRANSACTIONS
-- =========================================
CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT NOT NULL,
    transaction_date DATE NOT NULL,
    purchase_amount REAL DEFAULT 0,
    redemption_amount REAL DEFAULT 0,
    net_inflow REAL,
    transaction_type TEXT,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
        ON DELETE CASCADE
);

-- =========================================
-- 4. FACT TABLE: SCHEME PERFORMANCE
-- =========================================
CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT NOT NULL,
    performance_date DATE,
    returns_1m REAL,
    returns_3m REAL,
    returns_6m REAL,
    returns_1y REAL,
    returns_3y REAL,
    returns_5y REAL,
    sharpe_ratio REAL,
    volatility REAL,
    alpha REAL,
    beta REAL,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
        ON DELETE CASCADE
);

-- =========================================
-- 5. FACT TABLE: PORTFOLIO HOLDINGS
-- =========================================
CREATE TABLE fact_portfolio_holdings (
    holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT NOT NULL,
    holding_date DATE,
    company_name TEXT,
    sector TEXT,
    instrument_type TEXT,
    market_value REAL,
    holding_percent REAL,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
        ON DELETE CASCADE
);

-- =========================================
-- 6. DIMENSION TABLE: BENCHMARK INDICES
-- =========================================
CREATE TABLE dim_benchmark (
    benchmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    benchmark_name TEXT UNIQUE,
    index_provider TEXT,
    category TEXT
);

-- =========================================
-- 7. FACT TABLE: BENCHMARK RETURNS
-- =========================================
CREATE TABLE fact_benchmark_returns (
    benchmark_return_id INTEGER PRIMARY KEY AUTOINCREMENT,
    benchmark_id INTEGER,
    return_date DATE,
    index_value REAL,
    daily_return REAL,

    FOREIGN KEY (benchmark_id)
        REFERENCES dim_benchmark(benchmark_id)
        ON DELETE CASCADE
);

-- =========================================
-- 8. FACT TABLE: SIP INFLOWS
-- =========================================
CREATE TABLE fact_sip_inflows (
    sip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month_year TEXT,
    total_sip_accounts INTEGER,
    sip_amount REAL
);

-- =========================================
-- 9. FACT TABLE: CATEGORY INFLOWS
-- =========================================
CREATE TABLE fact_category_inflows (
    inflow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    month_year TEXT,
    inflow_amount REAL,
    outflow_amount REAL,
    net_flow REAL
);

-- =========================================
-- 10. FACT TABLE: FUND HOUSE AUM
-- =========================================
CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house TEXT,
    month_year TEXT,
    total_aum REAL,
    equity_aum REAL,
    debt_aum REAL,
    hybrid_aum REAL
);

