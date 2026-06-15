INSERT INTO dim_customer (
    customer_id,
    customer_name,
    email,
    phone,
    city,
    state,
    customer_segment,
    signup_date,
    loyalty_points
)
SELECT DISTINCT
    customer_id,
    customer_name,
    email,
    phone,
    city,
    state,
    customer_segment,
    signup_date,
    loyalty_points
FROM raw_customers;


INSERT INTO dim_product (
    product_id,
    product_name,
    category,
    brand,
    unit_price,
    cost_price,
    supplier,
    stock_quantity
)
SELECT DISTINCT
    product_id,
    product_name,
    category,
    brand,
    unit_price,
    cost_price,
    supplier,
    stock_quantity
FROM raw_products;


INSERT INTO dim_store (
    store_id,
    store_name,
    city,
    state,
    store_type,
    opening_date,
    manager_name
)
SELECT DISTINCT
    store_id,
    store_name,
    city,
    state,
    store_type,
    opening_date,
    manager_name
FROM raw_stores;


INSERT INTO dim_date (
    date_key,
    full_date,
    day,
    month,
    month_name,
    quarter,
    year
)
SELECT DISTINCT
    TO_CHAR(sale_date, 'YYYYMMDD')::INTEGER AS date_key,
    sale_date AS full_date,
    EXTRACT(DAY FROM sale_date)::INTEGER AS day,
    EXTRACT(MONTH FROM sale_date)::INTEGER AS month,
    TO_CHAR(sale_date, 'Month') AS month_name,
    EXTRACT(QUARTER FROM sale_date)::INTEGER AS quarter,
    EXTRACT(YEAR FROM sale_date)::INTEGER AS year
FROM raw_sales;


INSERT INTO fact_sales (
    sale_id,
    customer_key,
    product_key,
    store_key,
    date_key,
    quantity,
    unit_price,
    discount_percent,
    gross_amount,
    discount_amount,
    net_amount,
    cost_amount,
    profit_amount,
    payment_method,
    channel
)
SELECT
    rs.sale_id,
    dc.customer_key,
    dp.product_key,
    ds.store_key,
    dd.date_key,
    rs.quantity,
    dp.unit_price,
    rs.discount_percent,

    rs.quantity * dp.unit_price AS gross_amount,

    (rs.quantity * dp.unit_price) * (rs.discount_percent / 100.0) AS discount_amount,

    (rs.quantity * dp.unit_price)
        - ((rs.quantity * dp.unit_price) * (rs.discount_percent / 100.0)) AS net_amount,

    rs.quantity * dp.cost_price AS cost_amount,

    ((rs.quantity * dp.unit_price)
        - ((rs.quantity * dp.unit_price) * (rs.discount_percent / 100.0)))
        - (rs.quantity * dp.cost_price) AS profit_amount,

    rs.payment_method,
    rs.channel
FROM raw_sales rs
JOIN dim_customer dc
    ON rs.customer_id = dc.customer_id
JOIN dim_product dp
    ON rs.product_id = dp.product_id
JOIN dim_store ds
    ON rs.store_id = ds.store_id
JOIN dim_date dd
    ON rs.sale_date = dd.full_date;