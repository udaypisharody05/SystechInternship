DROP TABLE IF EXISTS raw_sales CASCADE;
DROP TABLE IF EXISTS raw_customers CASCADE;
DROP TABLE IF EXISTS raw_products CASCADE;
DROP TABLE IF EXISTS raw_stores CASCADE;

CREATE TABLE raw_customers (
    customer_id VARCHAR(10),
    customer_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    customer_segment VARCHAR(30),
    signup_date DATE,
    loyalty_points INTEGER
);

CREATE TABLE raw_products (
    product_id VARCHAR(10),
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    unit_price NUMERIC(10, 2),
    cost_price NUMERIC(10, 2),
    supplier VARCHAR(100),
    stock_quantity INTEGER
);

CREATE TABLE raw_stores (
    store_id VARCHAR(10),
    store_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    store_type VARCHAR(30),
    opening_date DATE,
    manager_name VARCHAR(100)
);

CREATE TABLE raw_sales (
    sale_id VARCHAR(20),
    customer_id VARCHAR(10),
    product_id VARCHAR(10),
    store_id VARCHAR(10),
    sale_date DATE,
    quantity INTEGER,
    discount_percent NUMERIC(5, 2),
    payment_method VARCHAR(30),
    channel VARCHAR(30)
);