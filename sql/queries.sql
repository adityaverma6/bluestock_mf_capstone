-- 1. Top five fund houses by latest reported AUM
WITH latest_aum AS (
    SELECT fund_house, aum_crore,
           ROW_NUMBER() OVER (PARTITION BY fund_house ORDER BY date DESC) AS row_num
    FROM fact_aum
)
SELECT fund_house, ROUND(aum_crore, 2) AS latest_aum_crore
FROM latest_aum
WHERE row_num = 1
ORDER BY latest_aum_crore DESC
LIMIT 5;

-- 2. Average NAV by month
SELECT substr(date, 1, 7) AS month, ROUND(AVG(nav), 2) AS average_nav
FROM fact_nav
GROUP BY month
ORDER BY month;

-- 3. SIP inflow trend
SELECT month, sip_inflow_crore, yoy_growth_pct
FROM fact_sip_inflows
ORDER BY month;

-- 4. Transaction activity by state
SELECT state,
       COUNT(*) AS transaction_count,
       ROUND(SUM(CASE WHEN transaction_type = 'Redemption'
                      THEN -amount_inr ELSE amount_inr END), 2) AS net_inflow_inr
FROM fact_transactions
GROUP BY state
ORDER BY net_inflow_inr DESC;

-- 5. Funds with an expense ratio below one percent
SELECT scheme_name, fund_house, category, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

-- 6. Top ten funds by one-year return
SELECT scheme_name, fund_house, return_1yr_pct
FROM fact_performance
ORDER BY return_1yr_pct DESC
LIMIT 10;

-- 7. Average one-year return by category
SELECT category, ROUND(AVG(return_1yr_pct), 2) AS average_1yr_return_pct
FROM fact_performance
GROUP BY category
ORDER BY average_1yr_return_pct DESC;

-- 8. Portfolio exposure by sector
SELECT sector, ROUND(SUM(weight_pct), 2) AS total_weight_pct
FROM fact_portfolio_holdings
GROUP BY sector
ORDER BY total_weight_pct DESC
LIMIT 10;

-- 9. Most volatile funds from derived NAV metrics
SELECT f.scheme_name, ROUND(m.annualized_volatility_pct, 2) AS volatility_pct
FROM fact_derived_metrics AS m
JOIN dim_fund AS f USING (amfi_code)
ORDER BY volatility_pct DESC
LIMIT 10;

-- 10. Benchmark date coverage
SELECT index_name,
       MIN(date) AS first_date,
       MAX(date) AS last_date,
       COUNT(*) AS observations
FROM fact_benchmark_returns
GROUP BY index_name
ORDER BY index_name;
