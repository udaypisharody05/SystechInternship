import psycopg2
from pathlib import Path
from db_config import DB_CONFIG


BASE_DIR = Path(__file__).resolve().parents[1]
SQL_FILES = [
    BASE_DIR / "sql" / "1_create_raw_tables.sql",
    BASE_DIR / "sql" / "2_create_warehouse_tables.sql",
]


def main():
    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            for sql_file in SQL_FILES:
                cursor.execute(sql_file.read_text(encoding="utf-8"))
                print(f"Executed {sql_file.name}")
    print("Raw, metadata, and warehouse tables created successfully.")


if __name__ == "__main__":
    main()
