-- Monthly revenue and profit
SELECT
    dd.year, dd.month, dd.month_name,
    SUM(fs.net_amount) AS total_revenue,
    SUM(fs.profit_amount) AS total_profit,
    COUNT(*) AS total_orders
FROM fact_sales fs
JOIN dim_date dd ON dd.date_key = fs.date_key
GROUP BY dd.year, dd.month, dd.month_name
ORDER BY dd.year, dd.month;

-- Sales by product category
SELECT
    dp.category,
    SUM(fs.quantity) AS total_quantity_sold,
    SUM(fs.net_amount) AS total_revenue,
    SUM(fs.profit_amount) AS total_profit
FROM fact_sales fs
JOIN dim_product dp ON dp.product_key = fs.product_key
GROUP BY dp.category
ORDER BY total_revenue DESC;

-- Revenue by store
SELECT
    ds.store_name, ds.city, ds.state, ds.store_type,
    SUM(fs.net_amount) AS total_revenue,
    SUM(fs.profit_amount) AS total_profit,
    COUNT(*) AS total_orders
FROM fact_sales fs
JOIN dim_store ds ON ds.store_key = fs.store_key
GROUP BY ds.store_name, ds.city, ds.state, ds.store_type
ORDER BY total_revenue DESC;

-- Payment-method summary using the new dimension
SELECT
    dpm.payment_method_name,
    COUNT(*) AS total_orders,
    SUM(fs.net_amount) AS total_revenue,
    SUM(fs.profit_amount) AS total_profit
FROM fact_sales fs
JOIN dim_payment_method dpm
  ON dpm.payment_method_key = fs.payment_method_key
GROUP BY dpm.payment_method_name
ORDER BY total_revenue DESC;

-- Incremental sales by batch
SELECT batch_id, COUNT(*) AS sales_count, SUM(net_amount) AS total_revenue
FROM fact_sales
GROUP BY batch_id
ORDER BY batch_id;
