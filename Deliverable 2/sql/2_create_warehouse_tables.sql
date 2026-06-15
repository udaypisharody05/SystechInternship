DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
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

    effective_start_date DATE NOT NULL,
    effective_end_date DATE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    UNIQUE (customer_id, effective_start_date)
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(10) NOT NULL,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    unit_price NUMERIC(10, 2),
    cost_price NUMERIC(10, 2),
    supplier VARCHAR(100),
    stock_quantity INTEGER,

    effective_start_date DATE NOT NULL,
    effective_end_date DATE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    UNIQUE (product_id, effective_start_date)
);

CREATE TABLE dim_store (
    store_key SERIAL PRIMARY KEY,
    store_id VARCHAR(10) NOT NULL,
    store_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    store_type VARCHAR(30),
    opening_date DATE,
    manager_name VARCHAR(100),

    effective_start_date DATE NOT NULL,
    effective_end_date DATE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    UNIQUE (store_id, effective_start_date)
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
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    product_key INTEGER REFERENCES dim_product(product_key),
    store_key INTEGER REFERENCES dim_store(store_key),
    date_key INTEGER REFERENCES dim_date(date_key),
    quantity INTEGER,
    unit_price NUMERIC(10, 2),
    discount_percent NUMERIC(5, 2),
    gross_amount NUMERIC(12, 2),
    discount_amount NUMERIC(12, 2),
    net_amount NUMERIC(12, 2),
    cost_amount NUMERIC(12, 2),
    profit_amount NUMERIC(12, 2),
    payment_method VARCHAR(30),
    channel VARCHAR(30)
);

CREATE INDEX idx_dim_customer_current
ON dim_customer(customer_id, is_current);

CREATE INDEX idx_dim_product_current
ON dim_product(product_id, is_current);

CREATE INDEX idx_dim_store_current
ON dim_store(store_id, is_current);