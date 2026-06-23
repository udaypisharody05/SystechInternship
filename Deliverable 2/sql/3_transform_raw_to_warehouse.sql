-- Simple Type 1 dimensions plus date and payment-method dimensions.
INSERT INTO dim_product (
    product_id, product_name, category, brand, unit_price,
    cost_price, supplier, stock_quantity
)
SELECT
    product_id, product_name, category, brand, unit_price,
    cost_price, supplier, stock_quantity
FROM raw_products
WHERE batch_id = %(batch_id)s
ON CONFLICT (product_id) DO UPDATE SET
    product_name = EXCLUDED.product_name,
    category = EXCLUDED.category,
    brand = EXCLUDED.brand,
    unit_price = EXCLUDED.unit_price,
    cost_price = EXCLUDED.cost_price,
    supplier = EXCLUDED.supplier,
    stock_quantity = EXCLUDED.stock_quantity,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dim_store (
    store_id, store_name, city, state, store_type, opening_date, manager_name
)
SELECT
    store_id, store_name, city, state, store_type, opening_date, manager_name
FROM raw_stores
WHERE batch_id = %(batch_id)s
ON CONFLICT (store_id) DO UPDATE SET
    store_name = EXCLUDED.store_name,
    city = EXCLUDED.city,
    state = EXCLUDED.state,
    store_type = EXCLUDED.store_type,
    opening_date = EXCLUDED.opening_date,
    manager_name = EXCLUDED.manager_name,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dim_payment_method (payment_method_name)
SELECT DISTINCT payment_method
FROM raw_sales
WHERE batch_id = %(batch_id)s
ON CONFLICT (payment_method_name) DO UPDATE SET
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dim_date (date_key, full_date, day, month, month_name, quarter, year)
SELECT DISTINCT
    TO_CHAR(sale_date, 'YYYYMMDD')::INTEGER,
    sale_date,
    EXTRACT(DAY FROM sale_date)::INTEGER,
    EXTRACT(MONTH FROM sale_date)::INTEGER,
    TRIM(TO_CHAR(sale_date, 'Month')),
    EXTRACT(QUARTER FROM sale_date)::INTEGER,
    EXTRACT(YEAR FROM sale_date)::INTEGER
FROM raw_sales
WHERE batch_id = %(batch_id)s
ON CONFLICT (date_key) DO NOTHING;
