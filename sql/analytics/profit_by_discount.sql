SELECT                
    discount,
    COUNT(*) AS nb_lines,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales), 4) AS profit_margin      
FROM 'data/processed/superstore_clean.parquet'
GROUP BY discount
ORDER BY discount ASC;