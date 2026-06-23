import subprocess
import sys
from pathlib import Path

import psycopg2

from db_config import DB_CONFIG


BASE_DIR = Path(__file__).resolve().parent


def run(script_name, *args):
    command = [sys.executable, str(BASE_DIR / script_name), *map(str, args)]
    print(f"\n> {' '.join(command)}")
    subprocess.run(command, check=True)


def print_query(title, query):
    print(f"\n{title}")
    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [description.name for description in cursor.description]
            print(" | ".join(columns))
            for row in cursor.fetchall():
                print(" | ".join(str(value) for value in row))


def show_snapshot(label):
    print_query(
        f"{label}: warehouse row counts",
        """
        SELECT 'dim_customer' AS table_name, COUNT(*) AS row_count
        FROM dim_customer
        UNION ALL
        SELECT 'dim_payment_method', COUNT(*) FROM dim_payment_method
        UNION ALL
        SELECT 'fact_sales', COUNT(*) FROM fact_sales
        ORDER BY table_name;
        """,
    )
    print_query(
        f"{label}: sales count by batch",
        """
        SELECT batch_id, COUNT(*) AS sales_count
        FROM fact_sales GROUP BY batch_id ORDER BY batch_id;
        """,
    )


def main():
    run("0_generate_raw_data.py")
    run("1_create_raw_tables.py")

    print("\n=== BATCH 1: INITIAL LOAD ===")
    run("2_load_raw_data.py", 1)
    run("3_run_transformations.py", 1)
    show_snapshot("After batch 1")

    print("\n=== BATCH 2: INCREMENTAL LOAD ===")
    run("2_load_raw_data.py", 2)
    run("3_run_transformations.py", 2)
    show_snapshot("After batch 2")

    print_query(
        "ETL metadata",
        "SELECT * FROM etl_metadata WHERE pipeline_name = 'sports_goods_elt';",
    )
    print_query(
        "Customer history for CUST001",
        """
        SELECT customer_key, customer_id, city, customer_segment,
               loyalty_points, effective_start_date, effective_end_date,
               is_current, source_batch_id
        FROM dim_customer
        WHERE customer_id = 'CUST001'
        ORDER BY effective_start_date;
        """,
    )
    print_query(
        "Payment method sales summary",
        """
        SELECT dpm.payment_method_name, COUNT(*) AS sales_count,
               SUM(fs.net_amount) AS total_revenue
        FROM fact_sales fs
        JOIN dim_payment_method dpm
          ON dpm.payment_method_key = fs.payment_method_key
        GROUP BY dpm.payment_method_name
        ORDER BY total_revenue DESC;
        """,
    )
    run("4_generate_reports.py")
    print("\nIncremental loading demo completed successfully.")


if __name__ == "__main__":
    main()
