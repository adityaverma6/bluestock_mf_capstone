PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code TEXT PRIMARY KEY,
    fund_house TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date TEXT,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code TEXT NOT NULL,
    date TEXT NOT NULL,
    nav REAL NOT NULL CHECK (nav > 0),
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    investor_id TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    amfi_code TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    amount_inr REAL NOT NULL CHECK (amount_inr >= 0),
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

CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code TEXT PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    category TEXT,
    plan TEXT,
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

CREATE TABLE IF NOT EXISTS fact_portfolio_holdings (
    amfi_code TEXT NOT NULL,
    stock_symbol TEXT,
    stock_name TEXT,
    sector TEXT,
    weight_pct REAL,
    market_value_cr REAL,
    current_price_inr REAL,
    portfolio_date TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_benchmark_returns (
    date TEXT NOT NULL,
    index_name TEXT NOT NULL,
    close_value REAL NOT NULL,
    PRIMARY KEY (date, index_name)
);

CREATE TABLE IF NOT EXISTS fact_sip_inflows (
    month TEXT PRIMARY KEY,
    sip_inflow_crore REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh REAL,
    sip_aum_lakh_crore REAL,
    yoy_growth_pct REAL
);

CREATE TABLE IF NOT EXISTS fact_category_inflows (
    month TEXT NOT NULL,
    category TEXT NOT NULL,
    net_inflow_crore REAL,
    PRIMARY KEY (month, category)
);

CREATE TABLE IF NOT EXISTS fact_aum (
    date TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,
    PRIMARY KEY (date, fund_house)
);

CREATE TABLE IF NOT EXISTS fact_industry_folios (
    month TEXT PRIMARY KEY,
    total_folios_crore REAL,
    equity_folios_crore REAL,
    debt_folios_crore REAL,
    hybrid_folios_crore REAL,
    others_folios_crore REAL
);

CREATE TABLE IF NOT EXISTS fact_derived_metrics (
    amfi_code TEXT PRIMARY KEY,
    observations INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    total_return_pct REAL,
    annualized_return_pct REAL,
    annualized_volatility_pct REAL,
    sharpe_ratio REAL,
    max_drawdown_pct REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE INDEX IF NOT EXISTS idx_nav_date ON fact_nav(date);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON fact_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_state ON fact_transactions(state);
CREATE INDEX IF NOT EXISTS idx_holdings_sector ON fact_portfolio_holdings(sector);
