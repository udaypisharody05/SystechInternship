# Overview of the day

Created a sample star schema in PostgreSQL consisting of dimension and fact tables for sales analytics.

## Tables Created

### Dimension Tables

* dim_customer
* dim_product
* dim_date

### Fact Table

* fact_sales

## Data Loaded

* 20 customer records
* 20 product records
* 20 date records
* 20 sales records

## Schema Design

The data model follows a star schema design with `fact_sales` as the central fact table connected to Customer, Product, and Date dimensions.

## Tools Used

* PostgreSQL 18
* DBeaver
