-- Latest successful batch
SELECT * FROM etl_metadata WHERE pipeline_name = 'sports_goods_elt';

-- SCD Type 2 history for the deliberately changed customer
SELECT
    customer_key, customer_id, city, state, customer_segment, loyalty_points,
    effective_start_date, effective_end_date, is_current, source_batch_id
FROM dim_customer
WHERE customer_id = 'CUST001'
ORDER BY effective_start_date;

-- Incremental fact counts
SELECT batch_id, COUNT(*) AS sales_count
FROM fact_sales
GROUP BY batch_id
ORDER BY batch_id;

-- Main warehouse row counts
SELECT 'dim_customer' AS table_name, COUNT(*) AS row_count FROM dim_customer
UNION ALL
SELECT 'dim_payment_method', COUNT(*) FROM dim_payment_method
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM fact_sales
ORDER BY table_name;

-- Payment-method sales summary
SELECT
    dpm.payment_method_name,
    COUNT(*) AS sales_count,
    SUM(fs.net_amount) AS total_revenue
FROM fact_sales fs
JOIN dim_payment_method dpm
  ON dpm.payment_method_key = fs.payment_method_key
GROUP BY dpm.payment_method_name
ORDER BY total_revenue DESC;

-- Basic correctness checks: both values should be zero
SELECT COUNT(*) AS duplicate_sale_ids
FROM (
    SELECT sale_id FROM fact_sales GROUP BY sale_id HAVING COUNT(*) > 1
) duplicates;

SELECT COUNT(*) AS customers_without_exactly_one_current_row
FROM (
    SELECT customer_id
    FROM dim_customer
    GROUP BY customer_id
    HAVING COUNT(*) FILTER (WHERE is_current) <> 1
) invalid_customers;
