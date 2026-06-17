# Deliverable 2: Sports Goods Store ELT Pipeline

## Objective

This project implements an ELT pipeline for a sports goods retail store. The pipeline extracts raw business data, loads it into PostgreSQL staging tables, transforms it into a data warehouse schema, and generates business reports.

## Business Scenario

The project simulates a sports goods store that sells products across categories such as cricket, football, badminton, tennis, fitness, running, swimming, sportswear, and accessories.

## ELT Pipeline Flow

Raw CSV Data  
→ Load into PostgreSQL Raw Tables  
→ Transform into Warehouse Tables  
→ Generate Business Reports  

## Dataset

The project uses generated raw CSV data:

- 50 customers
- 40 products
- 10 stores
- 200 sales transactions

## Database Layers

### Raw/Staging Tables

- raw_customers
- raw_products
- raw_stores
- raw_sales

### Data Warehouse Tables

- dim_customer
- dim_product
- dim_store
- dim_date
- fact_sales

## Scripts

| Script | Purpose |
|---|---|
| 0_generate_raw_data.py | Generates raw CSV files |
| 1_create_raw_tables.py | Creates PostgreSQL raw tables |
| 2_load_raw_data.py | Loads CSV data into raw tables |
| 3_run_transformations.py | Creates warehouse tables and transforms raw data |
| 4_generate_reports.py | Generates business reports |
| run_pipeline.py | Runs the full ELT pipeline end-to-end |

## SCD Type 2 Implementation

The project implements true Slowly Changing Dimension Type 2 logic for customer, product, and store dimensions.

The SCD Type 2 workflow includes:

1. Comparing incoming raw records with current dimension records.
2. Detecting changes in tracked attributes.
3. Expiring old current records by setting `is_current = false`.
4. Updating `effective_end_date` for expired records.
5. Inserting a new current record with updated values.
6. Preserving historical versions of dimension records.

The following scripts support SCD Type 2:

| Script | Purpose |
|---|---|
| `5_apply_scd2_changes.py` | Applies SCD Type 2 change detection and history preservation |
| `6_simulate_source_changes.py` | Simulates changes in source/raw tables for testing SCD Type 2 behavior |

This enables the warehouse to maintain historical changes such as customer segment changes, product price changes, and store manager updates.

## Reports Generated

- monthly_revenue.csv
- sales_by_category.csv
- top_selling_products.csv
- revenue_by_store.csv
- revenue_by_channel.csv

## Technologies Used

- Python
- PostgreSQL
- SQL
- Pandas
- psycopg2
- DBeaver

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt