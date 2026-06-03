-- =========================================
-- 1. TOP 5 FUNDS BY AUM
-- =========================================
SELECT 
    fund_house,
    MAX(total_aum) AS highest_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY highest_aum DESC
LIMIT 5;


-- =========================================
-- 2. AVERAGE NAV PER MONTH
-- =========================================
SELECT 
    strftime('%Y-%m', nav_date) AS month,
    ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month;


-- =========================================
-- 3. SIP YEAR-OVER-YEAR GROWTH
-- =========================================
SELECT
    substr(month_year, 1, 4) AS year,
    SUM(sip_amount) AS total_sip,
    ROUND(
        (
            SUM(sip_amount) -
            LAG(SUM(sip_amount)) OVER (
                ORDER BY substr(month_year,1,4)
            )
        ) * 100.0 /
        LAG(SUM(sip_amount)) OVER (
            ORDER BY substr(month_year,1,4)
        ),
        2
    ) AS yoy_growth_percent
FROM fact_sip_inflows
GROUP BY year;


-- =========================================
-- 4. TRANSACTIONS BY STATES
-- =========================================
SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(net_inflow) AS total_inflow
FROM fact_transactions
GROUP BY state
ORDER BY total_inflow DESC;


-- =========================================
-- 5. FUNDS WITH EXPENSE RATIO < 1%
-- =========================================
SELECT
    scheme_name,
    fund_house,
    category,
    expense_ratio
FROM dim_fund
WHERE expense_ratio < 1
ORDER BY expense_ratio ASC;


-- =========================================
-- 6. TOP 10 FUNDS BY 1-YEAR RETURN
-- =========================================
SELECT
    d.scheme_name,
    d.fund_house,
    p.returns_1y
FROM fact_performance p
JOIN dim_fund d
ON p.amfi_code = d.amfi_code
ORDER BY p.returns_1y DESC
LIMIT 10;


-- =========================================
-- 7. CATEGORY-WISE AVERAGE RETURNS
-- =========================================
SELECT
    d.category,
    ROUND(AVG(p.returns_1y), 2) AS avg_1y_return
FROM fact_performance p
JOIN dim_fund d
ON p.amfi_code = d.amfi_code
GROUP BY d.category
ORDER BY avg_1y_return DESC;


-- =========================================
-- 8. TOP SECTORS BY PORTFOLIO HOLDINGS
-- =========================================
SELECT
    sector,
    ROUND(SUM(holding_percent), 2) AS total_exposure
FROM fact_portfolio_holdings
GROUP BY sector
ORDER BY total_exposure DESC
LIMIT 10;


-- =========================================
-- 9. MOST VOLATILE FUNDS
-- =========================================
SELECT
    d.scheme_name,
    p.volatility
FROM fact_performance p
JOIN dim_fund d
ON p.amfi_code = d.amfi_code
ORDER BY p.volatility DESC
LIMIT 10;


-- =========================================
-- 10. BENCHMARK PERFORMANCE ANALYSIS
-- =========================================
SELECT
    b.benchmark_name,
    ROUND(AVG(r.daily_return), 2) AS avg_daily_return
FROM fact_benchmark_returns r
JOIN dim_benchmark b
ON r.benchmark_id = b.benchmark_id
GROUP BY b.benchmark_name
ORDER BY avg_daily_return DESC;
