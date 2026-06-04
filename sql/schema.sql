

PRAGMA foreign_keys = ON;

-- =========================================
-- 1. DIMENSION TABLE: FUND MASTER
-- =========================================
CREATE TABLE dim_fund (
    amfi_code TEXT PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date DATE,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

-- =========================================
-- 2. FACT TABLE: NAV HISTORY
-- =========================================
CREATE TABLE fact_nav (
    amfi_code TEXT,
    nav_date DATE,
    nav REAL,
    daily_return REAL,
    PRIMARY KEY (amfi_code, nav_date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- =========================================
-- 3. FACT TABLE: INVESTOR TRANSACTIONS
-- =========================================
CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    transaction_date DATE,
    amfi_code TEXT,
    transaction_type TEXT,
    amount_inr REAL,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- =========================================
-- 4. FACT TABLE: SCHEME PERFORMANCE
-- =========================================
CREATE TABLE fact_performance (
    amfi_code TEXT PRIMARY KEY,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    aum_crore REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
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
    aum_date DATE,
    fund_house TEXT,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,
    PRIMARY KEY (aum_date, fund_house)
);

