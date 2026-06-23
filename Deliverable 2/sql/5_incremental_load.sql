-- Customer SCD Type 2 and incremental fact load for one batch.
WITH batch_time AS (
    SELECT MIN(created_at) AS effective_at
    FROM raw_customers
    WHERE batch_id = %(batch_id)s
)
UPDATE dim_customer dc
SET
    effective_end_date = bt.effective_at,
    is_current = FALSE,
    updated_at = CURRENT_TIMESTAMP
FROM raw_customers rc
CROSS JOIN batch_time bt
WHERE rc.batch_id = %(batch_id)s
  AND dc.customer_id = rc.customer_id
  AND dc.is_current = TRUE
  AND (
      dc.customer_name IS DISTINCT FROM rc.customer_name OR
      dc.email IS DISTINCT FROM rc.email OR
      dc.phone IS DISTINCT FROM rc.phone OR
      dc.city IS DISTINCT FROM rc.city OR
      dc.state IS DISTINCT FROM rc.state OR
      dc.customer_segment IS DISTINCT FROM rc.customer_segment OR
      dc.signup_date IS DISTINCT FROM rc.signup_date OR
      dc.loyalty_points IS DISTINCT FROM rc.loyalty_points
  );

INSERT INTO dim_customer (
    customer_id, customer_name, email, phone, city, state,
    customer_segment, signup_date, loyalty_points,
    effective_start_date, effective_end_date, is_current, source_batch_id
)
SELECT
    rc.customer_id, rc.customer_name, rc.email, rc.phone, rc.city, rc.state,
    rc.customer_segment, rc.signup_date, rc.loyalty_points,
    rc.created_at, NULL, TRUE, rc.batch_id
FROM raw_customers rc
LEFT JOIN dim_customer dc
    ON dc.customer_id = rc.customer_id
   AND dc.is_current = TRUE
WHERE rc.batch_id = %(batch_id)s
  AND dc.customer_key IS NULL;

INSERT INTO fact_sales (
    sale_id, customer_key, product_key, store_key, payment_method_key,
    date_key, quantity, unit_price, discount_percent,
    gross_amount, discount_amount, net_amount, cost_amount,
    profit_amount, channel, batch_id
)
SELECT
    rs.sale_id,
    dc.customer_key,
    dp.product_key,
    ds.store_key,
    dpm.payment_method_key,
    dd.date_key,
    rs.quantity,
    dp.unit_price,
    rs.discount_percent,
    rs.quantity * dp.unit_price,
    (rs.quantity * dp.unit_price) * (rs.discount_percent / 100.0),
    (rs.quantity * dp.unit_price) * (1 - rs.discount_percent / 100.0),
    rs.quantity * dp.cost_price,
    (rs.quantity * dp.unit_price) * (1 - rs.discount_percent / 100.0)
        - (rs.quantity * dp.cost_price),
    rs.channel,
    rs.batch_id
FROM raw_sales rs
JOIN dim_customer dc
    ON dc.customer_id = rs.customer_id AND dc.is_current = TRUE
JOIN dim_product dp ON dp.product_id = rs.product_id
JOIN dim_store ds ON ds.store_id = rs.store_id
JOIN dim_payment_method dpm ON dpm.payment_method_name = rs.payment_method
JOIN dim_date dd ON dd.full_date = rs.sale_date
WHERE rs.batch_id = %(batch_id)s
ON CONFLICT (sale_id) DO NOTHING;

UPDATE etl_metadata
SET
    last_successful_batch_id = %(batch_id)s,
    last_successful_load = CURRENT_TIMESTAMP,
    updated_at = CURRENT_TIMESTAMP
WHERE pipeline_name = 'sports_goods_elt';
