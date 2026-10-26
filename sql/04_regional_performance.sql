
-- Project: Sales Performance Analysis
-- Purpose: Compare sales and profitability across regions and states.

CREATE OR REPLACE VIEW analytics.vw_regional_performance AS
SELECT
    region,
    state_province,
    SUM(sales) AS total_revenue,
    SUM(profit) AS total_profit,
    ROUND(
        100.0 * SUM(profit) / NULLIF(SUM(sales), 0),
        2
    ) AS profit_margin_pct,
    COUNT(DISTINCT order_id) AS total_orders
FROM analytics.sales_clean
GROUP BY
    region,
    state_province;
