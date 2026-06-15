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