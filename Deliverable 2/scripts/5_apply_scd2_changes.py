import psycopg2
from pathlib import Path
from db_config import DB_CONFIG


BASE_DIR = Path(__file__).resolve().parents[1]
SQL_FILE = BASE_DIR / "sql" / "5_apply_scd2_changes.sql"


def run_sql_file(cursor, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        sql_script = file.read()
        cursor.execute(sql_script)

    print(f"Executed {file_path.name}")


def main():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        run_sql_file(cursor, SQL_FILE)

        connection.commit()
        print("SCD Type 2 changes applied successfully.")

    except Exception as error:
        print("Error while applying SCD Type 2 changes:", error)

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals():
            connection.close()


if __name__ == "__main__":
    main()