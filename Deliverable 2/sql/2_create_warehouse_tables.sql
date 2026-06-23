DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS dim_payment_method CASCADE;
DROP TABLE IF EXISTS dim_store CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;

CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    customer_segment VARCHAR(30),
    signup_date DATE,
    loyalty_points INTEGER,
    effective_start_date TIMESTAMPTZ NOT NULL,
    effective_end_date TIMESTAMPTZ,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    source_batch_id INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uq_dim_customer_current
ON dim_customer(customer_id) WHERE is_current = TRUE;

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(10) UNIQUE NOT NULL,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    unit_price NUMERIC(10, 2),
    cost_price NUMERIC(10, 2),
    supplier VARCHAR(100),
    stock_quantity INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_store (
    store_key SERIAL PRIMARY KEY,
    store_id VARCHAR(10) UNIQUE NOT NULL,
    store_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    store_type VARCHAR(30),
    opening_date DATE,
    manager_name VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_payment_method (
    payment_method_key SERIAL PRIMARY KEY,
    payment_method_name VARCHAR(30) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    quarter INTEGER,
    year INTEGER
);

CREATE TABLE fact_sales (
    sales_key SERIAL PRIMARY KEY,
    sale_id VARCHAR(20) UNIQUE NOT NULL,
    customer_key INTEGER NOT NULL REFERENCES dim_customer(customer_key),
    product_key INTEGER NOT NULL REFERENCES dim_product(product_key),
    store_key INTEGER NOT NULL REFERENCES dim_store(store_key),
    payment_method_key INTEGER NOT NULL REFERENCES dim_payment_method(payment_method_key),
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    quantity INTEGER,
    unit_price NUMERIC(10, 2),
    discount_percent NUMERIC(5, 2),
    gross_amount NUMERIC(12, 2),
    discount_amount NUMERIC(12, 2),
    net_amount NUMERIC(12, 2),
    cost_amount NUMERIC(12, 2),
    profit_amount NUMERIC(12, 2),
    channel VARCHAR(30),
    batch_id INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
