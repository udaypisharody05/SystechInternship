import csv
import subprocess
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

import psycopg2

from db_config import DB_CONFIG


BASE_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"

CUSTOMER_HEADERS = [
    "customer_id", "customer_name", "email", "phone", "city", "state",
    "customer_segment", "signup_date", "loyalty_points",
]
PRODUCT_HEADERS = [
    "product_id", "product_name", "category", "brand", "unit_price",
    "cost_price", "supplier", "stock_quantity",
]
STORE_HEADERS = [
    "store_id", "store_name", "city", "state", "store_type",
    "opening_date", "manager_name",
]
SALES_HEADERS = [
    "sale_id", "customer_id", "product_id", "store_id", "sale_date",
    "quantity", "discount_percent", "payment_method", "channel",
]


def required(prompt, default=None, max_length=None):
    while True:
        suffix = f" [{default}]" if default not in (None, "") else ""
        value = input(f"{prompt}{suffix}: ").strip()
        if not value and default not in (None, ""):
            value = str(default)
        if value:
            if max_length is not None and len(value) > max_length:
                print(f"Enter at most {max_length} characters.")
                continue
            return value
        print("A value is required.")


def integer_value(prompt, default=None, minimum=0):
    while True:
        value = required(prompt, default)
        try:
            parsed = int(value)
            if parsed < minimum:
                raise ValueError
            return str(parsed)
        except ValueError:
            print(f"Enter an integer greater than or equal to {minimum}.")


def decimal_value(prompt, default=None, minimum=0, maximum=None):
    while True:
        value = required(prompt, default)
        try:
            parsed = Decimal(value)
            if parsed < minimum or (maximum is not None and parsed > maximum):
                raise ValueError
            return str(parsed)
        except (InvalidOperation, ValueError):
            limit = f" and at most {maximum}" if maximum is not None else ""
            print(f"Enter a number greater than or equal to {minimum}{limit}.")


def date_value(prompt, default=None):
    while True:
        value = required(prompt, default)
        try:
            date.fromisoformat(value)
            return value
        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")


def fetch_one(connection, query, parameters=()):
    with connection.cursor() as cursor:
        cursor.execute(query, parameters)
        return cursor.fetchone()


def customer_exists(connection, customer_id):
    return fetch_one(
        connection,
        """
        SELECT 1
        FROM dim_customer
        WHERE customer_id = %s AND is_current = TRUE;
        """,
        (customer_id,),
    ) is not None


def add_customer(connection, customer_rows):
    existing_batch_ids = {row[0] for row in customer_rows}
    while True:
        customer_id = required("Customer ID", max_length=10)
        if customer_id in existing_batch_ids or customer_exists(connection, customer_id):
            print("That customer ID already exists. Use the update option instead.")
            continue
        break

    customer_rows.append([
        customer_id,
        required("Customer name"),
        required("Email"),
        required("Phone"),
        required("City"),
        required("State"),
        required("Customer segment"),
        date_value("Signup date"),
        integer_value("Loyalty points", minimum=0),
    ])
    print(f"Staged new customer {customer_id}.")


def update_customer(connection, customer_rows, updated_customer_ids):
    customer_id = required("Existing customer ID", max_length=10)
    row = fetch_one(
        connection,
        """
        SELECT customer_id, customer_name, email, phone, city, state,
               customer_segment, signup_date, loyalty_points
        FROM dim_customer
        WHERE customer_id = %s AND is_current = TRUE;
        """,
        (customer_id,),
    )
    if row is None:
        print("No current customer was found with that ID.")
        return

    values = ["" if value is None else str(value) for value in row]
    replacement = [
        customer_id,
        required("Customer name", values[1]),
        required("Email", values[2]),
        required("Phone", values[3]),
        required("City", values[4]),
        required("State", values[5]),
        required("Customer segment", values[6]),
        date_value("Signup date", values[7]),
        integer_value("Loyalty points", values[8], minimum=0),
    ]

    customer_rows[:] = [item for item in customer_rows if item[0] != customer_id]
    customer_rows.append(replacement)
    updated_customer_ids.add(customer_id)
    print(f"Staged update for customer {customer_id}.")


def dimension_value_exists(connection, table, column, value):
    allowed = {
        ("dim_product", "product_id"),
        ("dim_store", "store_id"),
        ("dim_payment_method", "payment_method_name"),
    }
    if (table, column) not in allowed:
        raise ValueError("Unsupported dimension lookup.")
    return fetch_one(
        connection,
        f"SELECT 1 FROM {table} WHERE {column} = %s;",
        (value,),
    ) is not None


def add_sale(connection, customer_rows, sale_rows):
    staged_customers = {row[0] for row in customer_rows}

    while True:
        sale_id = required("Sale ID", max_length=20)
        duplicate = fetch_one(
            connection, "SELECT 1 FROM fact_sales WHERE sale_id = %s;", (sale_id,)
        )
        if duplicate or any(row[0] == sale_id for row in sale_rows):
            print("That sale ID already exists.")
            continue
        break

    while True:
        customer_id = required("Customer ID", max_length=10)
        if customer_id in staged_customers or customer_exists(connection, customer_id):
            break
        print("Customer ID does not exist. Add the customer to this batch first.")

    while True:
        product_id = required("Product ID", max_length=10)
        if dimension_value_exists(connection, "dim_product", "product_id", product_id):
            break
        print("Product ID does not exist in dim_product.")

    while True:
        store_id = required("Store ID", max_length=10)
        if dimension_value_exists(connection, "dim_store", "store_id", store_id):
            break
        print("Store ID does not exist in dim_store.")

    payment_method = required("Payment method", max_length=30)
    if not dimension_value_exists(
        connection, "dim_payment_method", "payment_method_name", payment_method
    ):
        print(f"'{payment_method}' will be added to dim_payment_method by this batch.")

    sale_rows.append([
        sale_id,
        customer_id,
        product_id,
        store_id,
        date_value("Sale date"),
        integer_value("Quantity", minimum=1),
        decimal_value("Discount percent", default="0", minimum=0, maximum=100),
        payment_method,
        required("Channel"),
    ])
    print(f"Staged new sale {sale_id}.")


def write_csv(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def print_query(connection, title, query, parameters=()):
    print(f"\n{title}")
    with connection.cursor() as cursor:
        cursor.execute(query, parameters)
        columns = [description.name for description in cursor.description]
        print(" | ".join(columns))
        for row in cursor.fetchall():
            print(" | ".join(str(value) for value in row))


def run_pipeline(batch_id):
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "2_load_raw_data.py"), str(batch_id)],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "3_run_transformations.py"), str(batch_id)],
        check=True,
    )


def main():
    customer_rows = []
    sale_rows = []
    updated_customer_ids = set()

    with psycopg2.connect(**DB_CONFIG) as connection:
        metadata = fetch_one(
            connection,
            """
            SELECT last_successful_batch_id
            FROM etl_metadata
            WHERE pipeline_name = 'sports_goods_elt';
            """,
        )
        if metadata is None:
            raise RuntimeError("etl_metadata is not initialized.")

        batch_id = metadata[0] + 1
        batch_dir = RAW_DIR / f"batch_{batch_id:03d}"
        if batch_dir.exists():
            raise FileExistsError(
                f"{batch_dir} already exists. Remove it only if this batch has not "
                "been loaded, then run the script again."
            )

        print(f"Creating manual batch {batch_id:03d}.")
        while True:
            print(
                "\n1. Add a new customer\n"
                "2. Update an existing customer\n"
                "3. Add a new sale\n"
                "4. Finish and load batch"
            )
            choice = input("Choose an option: ").strip()
            if choice == "1":
                add_customer(connection, customer_rows)
            elif choice == "2":
                update_customer(connection, customer_rows, updated_customer_ids)
            elif choice == "3":
                add_sale(connection, customer_rows, sale_rows)
            elif choice == "4":
                if customer_rows or sale_rows:
                    break
                print("Add at least one customer change or sale before finishing.")
            else:
                print("Choose 1, 2, 3, or 4.")

    batch_dir.mkdir(parents=True)
    write_csv(batch_dir / "customers.csv", CUSTOMER_HEADERS, customer_rows)
    write_csv(batch_dir / "products.csv", PRODUCT_HEADERS, [])
    write_csv(batch_dir / "stores.csv", STORE_HEADERS, [])
    write_csv(batch_dir / "sales.csv", SALES_HEADERS, sale_rows)
    print(f"\nWrote manual CSV batch to {batch_dir}")

    run_pipeline(batch_id)

    with psycopg2.connect(**DB_CONFIG) as connection:
        print_query(
            connection,
            "ETL metadata",
            "SELECT * FROM etl_metadata WHERE pipeline_name = 'sports_goods_elt';",
        )
        for customer_id in sorted(updated_customer_ids):
            print_query(
                connection,
                f"Customer history for {customer_id}",
                """
                SELECT customer_key, customer_id, city, state, customer_segment,
                       loyalty_points, effective_start_date, effective_end_date,
                       is_current, source_batch_id
                FROM dim_customer
                WHERE customer_id = %s
                ORDER BY effective_start_date;
                """,
                (customer_id,),
            )
        print_query(
            connection,
            "Sales count by batch_id",
            """
            SELECT batch_id, COUNT(*) AS sales_count
            FROM fact_sales
            GROUP BY batch_id
            ORDER BY batch_id;
            """,
        )
        print_query(
            connection,
            "Total fact_sales count",
            "SELECT COUNT(*) AS total_fact_sales FROM fact_sales;",
        )


if __name__ == "__main__":
    main()
