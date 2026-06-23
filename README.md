# Deliverable 2: Incremental PostgreSQL ELT Pipeline

This project demonstrates a two-batch ELT pipeline for a sports-goods retailer.
It loads CSV data into PostgreSQL raw tables and incrementally populates a
small star schema.

## Demo data

`0_generate_raw_data.py` creates immutable batch folders:

- `batch_001`: 100 customers, 50 products, 10 stores, and 500 sales.
- `batch_002`: one changed customer (`CUST001`), 10 new customers, and
  100 new sales.

The generator uses a fixed random seed, so the demo is reproducible.

## Database design

Raw tables:

- `raw_customers`
- `raw_products`
- `raw_stores`
- `raw_sales`

Every raw table includes `batch_id`, `created_at`, and `updated_at`.
Rows are unique within a batch and raw loads use an upsert, making staging
reloads safe.

Warehouse tables:

- `dim_customer` — true SCD Type 2
- `dim_product` — simple Type 1 upsert
- `dim_store` — simple Type 1 upsert
- `dim_payment_method` — incrementally populated from sales
- `dim_date`
- `fact_sales` — incremental, with a unique `sale_id` and source `batch_id`
- `etl_metadata` — tracks the last successful batch and load timestamp

## Customer SCD Type 2

For each incoming batch, customer attributes are compared using PostgreSQL
`IS DISTINCT FROM`, which handles nullable values safely.

When a current customer changes:

1. The old row receives an `effective_end_date` and `is_current = false`.
2. A new row is inserted with a new surrogate key.
3. Existing facts continue to reference the historical customer row.
4. New facts reference the new current row.

A partial unique index guarantees at most one current row per customer.

## Install

Run from the repository root:

```powershell
pip install -r requirements.txt
```

Database connection settings are currently in
`Deliverable 2/scripts/db_config.py`. Ensure the configured PostgreSQL
database exists and is reachable.

## Run the complete two-batch demo

Warning: the setup step drops and recreates this deliverable's raw and
warehouse tables.

```powershell
python "Deliverable 2/scripts/demo_incremental_load.py"
```

The demo prints:

- Warehouse row counts after batch 1 and batch 2
- Sales counts grouped by `batch_id`
- `etl_metadata`
- Both SCD2 versions of `CUST001`
- Payment-method sales totals

It also regenerates report CSVs under `Deliverable 2/reports/`.

## Run the stages manually

```powershell
python "Deliverable 2/scripts/0_generate_raw_data.py"
python "Deliverable 2/scripts/1_create_raw_tables.py"
python "Deliverable 2/scripts/2_load_raw_data.py" 1
python "Deliverable 2/scripts/3_run_transformations.py" 1
python "Deliverable 2/scripts/2_load_raw_data.py" 2
python "Deliverable 2/scripts/3_run_transformations.py" 2
python "Deliverable 2/scripts/4_generate_reports.py"
```

Batch transformations must run in sequence. The metadata check rejects batch
2 before batch 1 and rejects a transformation batch that has already
completed.

## Validation SQL

```powershell
psql -U postgres -d systech -f "Deliverable 2/sql/6_validation_queries.sql"
```

The validation queries show metadata, `CUST001` history, sales by batch,
warehouse counts, payment-method totals, duplicate sales, and invalid current
customer counts.
