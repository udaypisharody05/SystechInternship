from pathlib import Path

import pandas as pd
import psycopg2

from db_config import DB_CONFIG


BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

REPORT_QUERIES = {
    "monthly_revenue.csv": """
        SELECT dd.year, dd.month, dd.month_name,
               SUM(fs.net_amount) AS total_revenue,
               SUM(fs.profit_amount) AS total_profit,
               COUNT(*) AS total_orders
        FROM fact_sales fs
        JOIN dim_date dd ON dd.date_key = fs.date_key
        GROUP BY dd.year, dd.month, dd.month_name
        ORDER BY dd.year, dd.month;
    """,
    "sales_by_category.csv": """
        SELECT dp.category, SUM(fs.quantity) AS total_quantity_sold,
               SUM(fs.net_amount) AS total_revenue,
               SUM(fs.profit_amount) AS total_profit
        FROM fact_sales fs
        JOIN dim_product dp ON dp.product_key = fs.product_key
        GROUP BY dp.category
        ORDER BY total_revenue DESC;
    """,
    "top_selling_products.csv": """
        SELECT dp.product_name, dp.category, dp.brand,
               SUM(fs.quantity) AS total_quantity_sold,
               SUM(fs.net_amount) AS total_revenue
        FROM fact_sales fs
        JOIN dim_product dp ON dp.product_key = fs.product_key
        GROUP BY dp.product_name, dp.category, dp.brand
        ORDER BY total_quantity_sold DESC
        LIMIT 10;
    """,
    "revenue_by_store.csv": """
        SELECT ds.store_name, ds.city, ds.state, ds.store_type,
               SUM(fs.net_amount) AS total_revenue,
               SUM(fs.profit_amount) AS total_profit,
               COUNT(*) AS total_orders
        FROM fact_sales fs
        JOIN dim_store ds ON ds.store_key = fs.store_key
        GROUP BY ds.store_name, ds.city, ds.state, ds.store_type
        ORDER BY total_revenue DESC;
    """,
    "revenue_by_payment_method.csv": """
        SELECT dpm.payment_method_name, COUNT(*) AS total_orders,
               SUM(fs.net_amount) AS total_revenue,
               SUM(fs.profit_amount) AS total_profit
        FROM fact_sales fs
        JOIN dim_payment_method dpm
          ON dpm.payment_method_key = fs.payment_method_key
        GROUP BY dpm.payment_method_name
        ORDER BY total_revenue DESC;
    """,
}


def main():
    with psycopg2.connect(**DB_CONFIG) as connection:
        for file_name, query in REPORT_QUERIES.items():
            frame = pd.read_sql_query(query, connection)
            frame.to_csv(REPORTS_DIR / file_name, index=False)
            print(f"Generated {file_name}")


if __name__ == "__main__":
    main()
