
-- Project: Sales Performance Analysis
-- Purpose: Analyze monthly sales and profitability trends.

CREATE OR REPLACE VIEW analytics.vw_monthly_performance AS
SELECT
    DATE_TRUNC('month', order_date)::DATE AS sales_month,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        100.0 * SUM(profit) / NULLIF(SUM(sales), 0),
        2
    ) AS profit_margin_pct
FROM analytics.sales_clean
GROUP BY DATE_TRUNC('month', order_date)::DATE;
