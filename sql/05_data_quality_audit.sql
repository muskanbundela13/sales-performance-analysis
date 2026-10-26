
-- Project: Sales Performance Analysis
-- Purpose: Validate record counts, missing values, and date quality.
-- Analysis reference date: 2026-10-26

-- 1. Check total records and date range.
SELECT
    COUNT(*) AS total_rows,
    MIN(order_date) AS earliest_order_date,
    MAX(order_date) AS latest_order_date,
    MIN(ship_date) AS earliest_ship_date,
    MAX(ship_date) AS latest_ship_date
FROM analytics.sales_clean;

-- 2. Check missing values in important columns.
SELECT
    COUNT(*) FILTER (WHERE order_id IS NULL) AS missing_order_ids,
    COUNT(*) FILTER (WHERE order_date IS NULL) AS missing_order_dates,
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS missing_customer_ids,
    COUNT(*) FILTER (WHERE sales IS NULL) AS missing_sales,
    COUNT(*) FILTER (WHERE profit IS NULL) AS missing_profit,
    COUNT(*) FILTER (WHERE quantity IS NULL) AS missing_quantity
FROM analytics.sales_clean;

-- 3. Identify order dates after the analysis reference date.
SELECT
    COUNT(*) AS future_dated_orders
FROM analytics.sales_clean
WHERE order_date > DATE '2026-10-26';

-- 4. Inspect the records with future order dates.
SELECT
    order_id,
    order_date,
    ship_date,
    sales,
    profit
FROM analytics.sales_clean
WHERE order_date > DATE '2026-10-26'
ORDER BY order_date
LIMIT 20;

-- 5. Check for shipping dates earlier than order dates.
SELECT
    COUNT(*) AS invalid_shipping_date_rows
FROM analytics.sales_clean
WHERE ship_date < order_date;
