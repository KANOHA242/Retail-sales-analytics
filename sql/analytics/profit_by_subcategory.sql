SELECT                
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales), 4) AS profit_margin,
    ROUND(AVG(discount), 2) AS avg_discount,
    ROUND(
    SUM(CASE WHEN discount = 0 THEN profit END)/ SUM(CASE WHEN discount = 0 THEN sales END), 4) AS margin_no_discount
FROM 'data/processed/superstore_clean.parquet'
GROUP BY category, sub_category
ORDER BY total_profit ASC;