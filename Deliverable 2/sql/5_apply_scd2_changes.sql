-- ============================================================
-- SCD TYPE 2 LOGIC FOR CUSTOMER DIMENSION
-- ============================================================

UPDATE dim_customer dc
SET
    effective_end_date = CURRENT_DATE - INTERVAL '1 day',
    is_current = FALSE
FROM raw_customers rc
WHERE dc.customer_id = rc.customer_id
  AND dc.is_current = TRUE
  AND (
        dc.customer_name <> rc.customer_name
        OR dc.email <> rc.email
        OR dc.phone <> rc.phone
        OR dc.city <> rc.city
        OR dc.state <> rc.state
        OR dc.customer_segment <> rc.customer_segment
        OR dc.signup_date <> rc.signup_date
        OR dc.loyalty_points <> rc.loyalty_points
  );

INSERT INTO dim_customer (
    customer_id,
    customer_name,
    email,
    phone,
    city,
    state,
    customer_segment,
    signup_date,
    loyalty_points,
    effective_start_date,
    effective_end_date,
    is_current
)
SELECT
    rc.customer_id,
    rc.customer_name,
    rc.email,
    rc.phone,
    rc.city,
    rc.state,
    rc.customer_segment,
    rc.signup_date,
    rc.loyalty_points,
    CURRENT_DATE AS effective_start_date,
    NULL::DATE AS effective_end_date,
    TRUE AS is_current
FROM raw_customers rc
LEFT JOIN dim_customer dc
    ON rc.customer_id = dc.customer_id
    AND dc.is_current = TRUE
WHERE dc.customer_id IS NULL;


-- ============================================================
-- SCD TYPE 2 LOGIC FOR PRODUCT DIMENSION
-- ============================================================

UPDATE dim_product dp
SET
    effective_end_date = CURRENT_DATE - INTERVAL '1 day',
    is_current = FALSE
FROM raw_products rp
WHERE dp.product_id = rp.product_id
  AND dp.is_current = TRUE
  AND (
        dp.product_name <> rp.product_name
        OR dp.category <> rp.category
        OR dp.brand <> rp.brand
        OR dp.unit_price <> rp.unit_price
        OR dp.cost_price <> rp.cost_price
        OR dp.supplier <> rp.supplier
        OR dp.stock_quantity <> rp.stock_quantity
  );

INSERT INTO dim_product (
    product_id,
    product_name,
    category,
    brand,
    unit_price,
    cost_price,
    supplier,
    stock_quantity,
    effective_start_date,
    effective_end_date,
    is_current
)
SELECT
    rp.product_id,
    rp.product_name,
    rp.category,
    rp.brand,
    rp.unit_price,
    rp.cost_price,
    rp.supplier,
    rp.stock_quantity,
    CURRENT_DATE AS effective_start_date,
    NULL::DATE AS effective_end_date,
    TRUE AS is_current
FROM raw_products rp
LEFT JOIN dim_product dp
    ON rp.product_id = dp.product_id
    AND dp.is_current = TRUE
WHERE dp.product_id IS NULL;


-- ============================================================
-- SCD TYPE 2 LOGIC FOR STORE DIMENSION
-- ============================================================

UPDATE dim_store ds
SET
    effective_end_date = CURRENT_DATE - INTERVAL '1 day',
    is_current = FALSE
FROM raw_stores rs
WHERE ds.store_id = rs.store_id
  AND ds.is_current = TRUE
  AND (
        ds.store_name <> rs.store_name
        OR ds.city <> rs.city
        OR ds.state <> rs.state
        OR ds.store_type <> rs.store_type
        OR ds.opening_date <> rs.opening_date
        OR ds.manager_name <> rs.manager_name
  );

INSERT INTO dim_store (
    store_id,
    store_name,
    city,
    state,
    store_type,
    opening_date,
    manager_name,
    effective_start_date,
    effective_end_date,
    is_current
)
SELECT
    rs.store_id,
    rs.store_name,
    rs.city,
    rs.state,
    rs.store_type,
    rs.opening_date,
    rs.manager_name,
    CURRENT_DATE AS effective_start_date,
    NULL::DATE AS effective_end_date,
    TRUE AS is_current
FROM raw_stores rs
LEFT JOIN dim_store ds
    ON rs.store_id = ds.store_id
    AND ds.is_current = TRUE
WHERE ds.store_id IS NULL;