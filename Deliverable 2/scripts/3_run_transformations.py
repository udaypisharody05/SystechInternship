import argparse
from pathlib import Path

import psycopg2

from db_config import DB_CONFIG


BASE_DIR = Path(__file__).resolve().parents[1]
SQL_FILES = [
    BASE_DIR / "sql" / "3_transform_raw_to_warehouse.sql",
    BASE_DIR / "sql" / "5_incremental_load.sql",
]


def main():
    parser = argparse.ArgumentParser(description="Transform one incremental batch.")
    parser.add_argument("batch_id", type=int)
    args = parser.parse_args()
    if args.batch_id < 1:
        parser.error("batch_id must be a positive integer")

    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT last_successful_batch_id
                FROM etl_metadata
                WHERE pipeline_name = 'sports_goods_elt';
                """
            )
            last_batch = cursor.fetchone()[0]
            expected_batch = last_batch + 1
            if args.batch_id != expected_batch:
                raise ValueError(
                    f"Expected batch {expected_batch}, received batch {args.batch_id}."
                )

            for sql_file in SQL_FILES:
                cursor.execute(
                    sql_file.read_text(encoding="utf-8"),
                    {"batch_id": args.batch_id},
                )
                print(f"Executed {sql_file.name} for batch {args.batch_id}")

    print(f"Batch {args.batch_id} transformed successfully.")


if __name__ == "__main__":
    main()
