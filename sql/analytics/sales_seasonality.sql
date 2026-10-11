SELECT               
    order_month,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales), 4) AS profit_margin, 
    COUNT(DISTINCT order_id) AS total_orders       
FROM 'data/processed/superstore_clean.parquet'
GROUP BY order_month
ORDER BY order_month