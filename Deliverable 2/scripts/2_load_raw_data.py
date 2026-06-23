import argparse
import csv
from pathlib import Path

import psycopg2

from db_config import DB_CONFIG


BASE_DIR = Path(__file__).resolve().parents[1]
CSV_TABLE_MAPPING = {
    "customers.csv": ("raw_customers", "customer_id"),
    "products.csv": ("raw_products", "product_id"),
    "stores.csv": ("raw_stores", "store_id"),
    "sales.csv": ("raw_sales", "sale_id"),
}


def load_csv(cursor, path, table_name, key_column, batch_id):
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        rows = [row + [batch_id] for row in reader]

    if not rows:
        print(f"Loaded 0 rows into {table_name}")
        return

    columns = headers + ["batch_id"]
    placeholders = ", ".join(["%s"] * len(columns))
    update_columns = [column for column in headers if column != key_column]
    updates = ", ".join(
        f"{column} = EXCLUDED.{column}" for column in update_columns
    )
    query = f"""
        INSERT INTO {table_name} ({", ".join(columns)})
        VALUES ({placeholders})
        ON CONFLICT (batch_id, {key_column}) DO UPDATE SET
            {updates},
            updated_at = CURRENT_TIMESTAMP;
    """
    cursor.executemany(query, rows)
    print(f"Loaded {len(rows)} rows into {table_name}")


def main():
    parser = argparse.ArgumentParser(description="Load one CSV batch into raw tables.")
    parser.add_argument("batch_id", type=int, choices=[1, 2])
    args = parser.parse_args()
    batch_dir = BASE_DIR / "data" / "raw" / f"batch_{args.batch_id:03d}"

    if not batch_dir.is_dir():
        raise FileNotFoundError(f"Batch folder not found: {batch_dir}")

    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            for file_name, (table_name, key_column) in CSV_TABLE_MAPPING.items():
                load_csv(
                    cursor, batch_dir / file_name, table_name, key_column,
                    args.batch_id,
                )
    print(f"Raw batch {args.batch_id} loaded successfully.")


if __name__ == "__main__":
    main()
