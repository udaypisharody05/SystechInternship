import csv
import psycopg2
from pathlib import Path
from db_config import DB_CONFIG


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


CSV_TABLE_MAPPING = {
    "customers.csv": "raw_customers",
    "products.csv": "raw_products",
    "stores.csv": "raw_stores",
    "sales.csv": "raw_sales"
}


def clear_raw_table(cursor, table_name):
    cursor.execute(f"TRUNCATE TABLE {table_name};")


def load_csv_to_table(cursor, csv_file_path, table_name):
    with open(csv_file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)

        columns = ", ".join(headers)
        placeholders = ", ".join(["%s"] * len(headers))

        insert_query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders});
        """

        rows = list(reader)
        cursor.executemany(insert_query, rows)

    print(f"Loaded {len(rows)} rows into {table_name}")


def main():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        for csv_file, table_name in CSV_TABLE_MAPPING.items():
            csv_file_path = RAW_DATA_DIR / csv_file

            clear_raw_table(cursor, table_name)
            load_csv_to_table(cursor, csv_file_path, table_name)

        connection.commit()
        print("Raw data loaded successfully.")

    except Exception as error:
        print("Error while loading raw data:", error)

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals():
            connection.close()


if __name__ == "__main__":
    main()