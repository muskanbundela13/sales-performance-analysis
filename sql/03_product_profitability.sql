
-- Project: Sales Performance Analysis
-- Purpose: Analyze profitability at product and subcategory level.

CREATE OR REPLACE VIEW analytics.vw_product_profitability AS
SELECT
    category,
    sub_category,
    product_id,
    product_name,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        100.0 * SUM(profit) / NULLIF(SUM(sales), 0),
        2
    ) AS profit_margin_pct,
    COUNT(*) FILTER (WHERE profit < 0) AS loss_making_lines
FROM analytics.sales_clean
GROUP BY
    category,
    sub_category,
    product_id,
    product_name;
