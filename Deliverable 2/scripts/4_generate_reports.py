import psycopg2
import pandas as pd
from pathlib import Path
from db_config import DB_CONFIG


BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


REPORT_QUERIES = {
    "monthly_revenue.csv": """
        SELECT
            dd.year,
            dd.month,
            TRIM(dd.month_name) AS month_name,
            SUM(fs.net_amount) AS total_revenue,
            SUM(fs.profit_amount) AS total_profit,
            COUNT(fs.sales_key) AS total_orders
        FROM fact_sales fs
        JOIN dim_date dd
            ON fs.date_key = dd.date_key
        GROUP BY dd.year, dd.month, dd.month_name
        ORDER BY dd.year, dd.month;
    """,

    "sales_by_category.csv": """
        SELECT
            dp.category,
            SUM(fs.quantity) AS total_quantity_sold,
            SUM(fs.net_amount) AS total_revenue,
            SUM(fs.profit_amount) AS total_profit
        FROM fact_sales fs
        JOIN dim_product dp
            ON fs.product_key = dp.product_key
        GROUP BY dp.category
        ORDER BY total_revenue DESC;
    """,

    "top_selling_products.csv": """
        SELECT
            dp.product_name,
            dp.category,
            dp.brand,
            SUM(fs.quantity) AS total_quantity_sold,
            SUM(fs.net_amount) AS total_revenue
        FROM fact_sales fs
        JOIN dim_product dp
            ON fs.product_key = dp.product_key
        GROUP BY dp.product_name, dp.category, dp.brand
        ORDER BY total_quantity_sold DESC
        LIMIT 10;
    """,

    "revenue_by_store.csv": """
        SELECT
            ds.store_name,
            ds.city,
            ds.state,
            ds.store_type,
            SUM(fs.net_amount) AS total_revenue,
            SUM(fs.profit_amount) AS total_profit,
            COUNT(fs.sales_key) AS total_orders
        FROM fact_sales fs
        JOIN dim_store ds
            ON fs.store_key = ds.store_key
        GROUP BY ds.store_name, ds.city, ds.state, ds.store_type
        ORDER BY total_revenue DESC;
    """,

    "revenue_by_channel.csv": """
        SELECT
            channel,
            COUNT(*) AS total_orders,
            SUM(net_amount) AS total_revenue,
            SUM(profit_amount) AS total_profit
        FROM fact_sales
        GROUP BY channel
        ORDER BY total_revenue DESC;
    """
}


def main():
    try:
        connection = psycopg2.connect(**DB_CONFIG)

        for file_name, query in REPORT_QUERIES.items():
            df = pd.read_sql_query(query, connection)
            output_path = REPORTS_DIR / file_name
            df.to_csv(output_path, index=False)
            print(f"Generated report: {output_path}")

        print("All reports generated successfully.")

    except Exception as error:
        print("Error while generating reports:", error)

    finally:
        if "connection" in locals():
            connection.close()


if __name__ == "__main__":
    main()