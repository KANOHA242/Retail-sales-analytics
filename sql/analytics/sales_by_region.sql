SELECT                
    region,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales), 4) AS profit_margin, 
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(discount), 2) AS avg_discount    
FROM 'data/processed/superstore_clean.parquet'
GROUP BY region
ORDER BY total_sales DESC;