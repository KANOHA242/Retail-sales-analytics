SELECT
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2)     AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(profit) / SUM(sales), 2) AS profit_margin,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM 'data/processed/superstore_clean.parquet'
