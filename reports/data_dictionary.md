# Mutual Fund Analytics Platform – Data Dictionary

## Database Name

`bluestock_mf.db`

## Database Type

SQLite Relational Database

---

# 1. Table: dim_fund

## Business Purpose

Stores master information about mutual fund schemes.

| Column Name   | Data Type | Business Definition                                | Source Reference        |
| ------------- | --------- | -------------------------------------------------- | ----------------------- |
| amfi_code     | TEXT      | Unique AMFI identifier for each mutual fund scheme | cleaned_fund_master.csv |
| scheme_name   | TEXT      | Name of the mutual fund scheme                     | cleaned_fund_master.csv |
| fund_house    | TEXT      | Asset Management Company (AMC) managing the fund   | cleaned_fund_master.csv |
| category      | TEXT      | Mutual fund category (Equity, Debt, Hybrid, etc.)  | cleaned_fund_master.csv |
| sub_category  | TEXT      | Detailed classification of the scheme              | cleaned_fund_master.csv |
| benchmark     | TEXT      | Benchmark index used to compare fund performance   | cleaned_fund_master.csv |
| launch_date   | DATE      | Date the fund was launched                         | cleaned_fund_master.csv |
| risk_level    | TEXT      | Risk profile of the scheme                         | cleaned_fund_master.csv |
| expense_ratio | REAL      | Annual operating expense charged by AMC            | cleaned_fund_master.csv |
| fund_manager  | TEXT      | Manager responsible for the scheme                 | cleaned_fund_master.csv |
| fund_type     | TEXT      | Open-ended / Close-ended classification            | cleaned_fund_master.csv |

---

# 2. Table: fact_nav

## Business Purpose

Stores historical Net Asset Value (NAV) records for mutual funds.

| Column Name  | Data Type | Business Definition              | Source Reference        |
| ------------ | --------- | -------------------------------- | ----------------------- |
| nav_id       | INTEGER   | Unique identifier for NAV record | System Generated        |
| amfi_code    | TEXT      | Mutual fund scheme identifier    | cleaned_nav_history.csv |
| nav_date     | DATE      | Date of NAV declaration          | cleaned_nav_history.csv |
| nav          | REAL      | Net Asset Value per unit         | cleaned_nav_history.csv |
| daily_return | REAL      | Daily percentage return of NAV   | Derived Metric          |

---

# 3. Table: fact_transactions

## Business Purpose

Stores investor purchase and redemption transaction information.

| Column Name       | Data Type | Business Definition                           | Source Reference                  |
| ----------------- | --------- | --------------------------------------------- | --------------------------------- |
| transaction_id    | INTEGER   | Unique transaction record identifier          | System Generated                  |
| amfi_code         | TEXT      | Mutual fund scheme identifier                 | cleaned_investor_transactions.csv |
| transaction_date  | DATE      | Date of investor transaction                  | cleaned_investor_transactions.csv |
| purchase_amount   | REAL      | Total amount invested by investors            | cleaned_investor_transactions.csv |
| redemption_amount | REAL      | Total redemption amount withdrawn             | cleaned_investor_transactions.csv |
| net_inflow        | REAL      | Net investment flow into the scheme           | Derived Metric                    |
| transaction_type  | TEXT      | Type of transaction (Purchase/Redemption/SIP) | cleaned_investor_transactions.csv |

---

# 4. Table: fact_performance

## Business Purpose

Stores scheme-level return and risk performance metrics.

| Column Name      | Data Type | Business Definition                  | Source Reference               |
| ---------------- | --------- | ------------------------------------ | ------------------------------ |
| performance_id   | INTEGER   | Unique performance record identifier | System Generated               |
| amfi_code        | TEXT      | Mutual fund scheme identifier        | cleaned_scheme_performance.csv |
| performance_date | DATE      | Date of performance calculation      | cleaned_scheme_performance.csv |
| returns_1m       | REAL      | One-month return percentage          | cleaned_scheme_performance.csv |
| returns_3m       | REAL      | Three-month return percentage        | cleaned_scheme_performance.csv |
| returns_6m       | REAL      | Six-month return percentage          | cleaned_scheme_performance.csv |
| returns_1y       | REAL      | One-year return percentage           | cleaned_scheme_performance.csv |
| returns_3y       | REAL      | Three-year annualized return         | cleaned_scheme_performance.csv |
| returns_5y       | REAL      | Five-year annualized return          | cleaned_scheme_performance.csv |
| sharpe_ratio     | REAL      | Risk-adjusted performance metric     | cleaned_scheme_performance.csv |
| volatility       | REAL      | Standard deviation of returns        | cleaned_scheme_performance.csv |
| alpha            | REAL      | Excess return over benchmark         | cleaned_scheme_performance.csv |
| beta             | REAL      | Sensitivity to market movement       | cleaned_scheme_performance.csv |

---

# 5. Table: fact_portfolio_holdings

## Business Purpose

Stores portfolio composition and sector allocation details.

| Column Name     | Data Type | Business Definition                 | Source Reference               |
| --------------- | --------- | ----------------------------------- | ------------------------------ |
| holding_id      | INTEGER   | Unique portfolio holding identifier | System Generated               |
| amfi_code       | TEXT      | Mutual fund scheme identifier       | cleaned_portfolio_holdings.csv |
| holding_date    | DATE      | Portfolio disclosure date           | cleaned_portfolio_holdings.csv |
| company_name    | TEXT      | Name of company/security held       | cleaned_portfolio_holdings.csv |
| sector          | TEXT      | Industry sector classification      | cleaned_portfolio_holdings.csv |
| instrument_type | TEXT      | Equity/Debt/Cash/ETF etc.           | cleaned_portfolio_holdings.csv |
| market_value    | REAL      | Market value of holding             | cleaned_portfolio_holdings.csv |
| holding_percent | REAL      | Percentage allocation in portfolio  | cleaned_portfolio_holdings.csv |

---

# 6. Table: dim_benchmark

## Business Purpose

Stores benchmark index master information.

| Column Name    | Data Type | Business Definition             | Source Reference              |
| -------------- | --------- | ------------------------------- | ----------------------------- |
| benchmark_id   | INTEGER   | Unique benchmark identifier     | System Generated              |
| benchmark_name | TEXT      | Name of benchmark index         | cleaned_benchmark_indices.csv |
| index_provider | TEXT      | Organization managing the index | cleaned_benchmark_indices.csv |
| category       | TEXT      | Benchmark category              | cleaned_benchmark_indices.csv |

---

# 7. Table: fact_benchmark_returns

## Business Purpose

Stores historical benchmark performance data.

| Column Name         | Data Type | Business Definition                | Source Reference              |
| ------------------- | --------- | ---------------------------------- | ----------------------------- |
| benchmark_return_id | INTEGER   | Unique benchmark return identifier | System Generated              |
| benchmark_id        | INTEGER   | Benchmark identifier               | cleaned_benchmark_indices.csv |
| return_date         | DATE      | Date of benchmark return           | cleaned_benchmark_indices.csv |
| index_value         | REAL      | Benchmark index closing value      | cleaned_benchmark_indices.csv |
| daily_return        | REAL      | Daily benchmark return percentage  | Derived Metric                |

---

# 8. Table: fact_sip_inflows

## Business Purpose

Stores SIP contribution statistics across the mutual fund industry.

| Column Name        | Data Type | Business Definition                 | Source Reference                |
| ------------------ | --------- | ----------------------------------- | ------------------------------- |
| sip_id             | INTEGER   | Unique SIP inflow record identifier | System Generated                |
| month_year         | TEXT      | Reporting month and year            | cleaned_monthly_sip_inflows.csv |
| total_sip_accounts | INTEGER   | Total active SIP accounts           | cleaned_monthly_sip_inflows.csv |
| sip_amount         | REAL      | Total SIP inflow amount             | cleaned_monthly_sip_inflows.csv |

---

# 9. Table: fact_category_inflows

## Business Purpose

Stores category-level fund inflow and outflow data.

| Column Name    | Data Type | Business Definition               | Source Reference             |
| -------------- | --------- | --------------------------------- | ---------------------------- |
| inflow_id      | INTEGER   | Unique category inflow identifier | System Generated             |
| category       | TEXT      | Mutual fund category              | cleaned_category_inflows.csv |
| month_year     | TEXT      | Reporting month and year          | cleaned_category_inflows.csv |
| inflow_amount  | REAL      | Total money invested              | cleaned_category_inflows.csv |
| outflow_amount | REAL      | Total money withdrawn             | cleaned_category_inflows.csv |
| net_flow       | REAL      | Net category inflow               | Derived Metric               |

---

# 10. Table: fact_aum

## Business Purpose

Stores Assets Under Management (AUM) statistics for fund houses.

| Column Name | Data Type | Business Definition           | Source Reference              |
| ----------- | --------- | ----------------------------- | ----------------------------- |
| aum_id      | INTEGER   | Unique AUM record identifier  | System Generated              |
| fund_house  | TEXT      | Asset Management Company name | cleaned_aum_by_fund_house.csv |
| month_year  | TEXT      | Reporting month and year      | cleaned_aum_by_fund_house.csv |
| total_aum   | REAL      | Total Assets Under Management | cleaned_aum_by_fund_house.csv |
| equity_aum  | REAL      | Equity mutual fund AUM        | cleaned_aum_by_fund_house.csv |
| debt_aum    | REAL      | Debt mutual fund AUM          | cleaned_aum_by_fund_house.csv |
| hybrid_aum  | REAL      | Hybrid mutual fund AUM        | cleaned_aum_by_fund_house.csv |

---

# Key Relationships

| Parent Table  | Child Table             | Relationship |
| ------------- | ----------------------- | ------------ |
| dim_fund      | fact_nav                | One-to-Many  |
| dim_fund      | fact_transactions       | One-to-Many  |
| dim_fund      | fact_performance        | One-to-Many  |
| dim_fund      | fact_portfolio_holdings | One-to-Many  |
| dim_benchmark | fact_benchmark_returns  | One-to-Many  |

---

# Data Sources

| Dataset                           | Description                  |
| --------------------------------- | ---------------------------- |
| cleaned_fund_master.csv           | Mutual fund master details   |
| cleaned_nav_history.csv           | Historical NAV data          |
| cleaned_investor_transactions.csv | Investor transaction records |
| cleaned_scheme_performance.csv    | Fund performance metrics     |
| cleaned_portfolio_holdings.csv    | Portfolio allocation data    |
| cleaned_benchmark_indices.csv     | Benchmark index information  |
| cleaned_monthly_sip_inflows.csv   | SIP inflow statistics        |
| cleaned_category_inflows.csv      | Category-wise inflows        |
| cleaned_aum_by_fund_house.csv     | Fund house AUM data          |
