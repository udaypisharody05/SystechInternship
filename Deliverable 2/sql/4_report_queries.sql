-- 1. Monthly revenue and profit
SELECT
    dd.year,
    dd.month,
    TRIM(dd.month_name) AS month_name,
    SUM(fs.net_amount) AS total_revenue,
    SUM(fs.profit_amount) AS total_profit,
    COUNT(fs.sales_key) AS total_orders
FROM fact_sales fs
JOIN dim_date dd
    ON fs.date_key = dd.date_key
GROUP BY dd.year, dd.month, dd.month_name
ORDER BY dd.year, dd.month;


-- 2. Sales by product category
SELECT
    dp.category,
    SUM(fs.quantity) AS total_quantity_sold,
    SUM(fs.net_amount) AS total_revenue,
    SUM(fs.profit_amount) AS total_profit
FROM fact_sales fs
JOIN dim_product dp
    ON fs.product_key = dp.product_key
GROUP BY dp.category
ORDER BY total_revenue DESC;


-- 3. Top 10 selling products
SELECT
    dp.product_name,
    dp.category,
    dp.brand,
    SUM(fs.quantity) AS total_quantity_sold,
    SUM(fs.net_amount) AS total_revenue
FROM fact_sales fs
JOIN dim_product dp
    ON fs.product_key = dp.product_key
GROUP BY dp.product_name, dp.category, dp.brand
ORDER BY total_quantity_sold DESC
LIMIT 10;


-- 4. Revenue by store
SELECT
    ds.store_name,
    ds.city,
    ds.state,
    ds.store_type,
    SUM(fs.net_amount) AS total_revenue,
    SUM(fs.profit_amount) AS total_profit,
    COUNT(fs.sales_key) AS total_orders
FROM fact_sales fs
JOIN dim_store ds
    ON fs.store_key = ds.store_key
GROUP BY ds.store_name, ds.city, ds.state, ds.store_type
ORDER BY total_revenue DESC;


-- 5. Revenue by sales channel
SELECT
    channel,
    COUNT(*) AS total_orders,
    SUM(net_amount) AS total_revenue,
    SUM(profit_amount) AS total_profit
FROM fact_sales
GROUP BY channel
ORDER BY total_revenue DESC;