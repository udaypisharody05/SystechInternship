import psycopg2
from db_config import DB_CONFIG


SOURCE_CHANGE_QUERIES = [
    """
    UPDATE raw_customers
    SET city = 'Mumbai',
        customer_segment = 'Premium',
        loyalty_points = loyalty_points + 500
    WHERE customer_id = 'C001';
    """,

    """
    UPDATE raw_products
    SET unit_price = unit_price + 250,
        stock_quantity = stock_quantity - 5
    WHERE product_id = 'P001';
    """,

    """
    UPDATE raw_stores
    SET manager_name = 'Rohit Menon',
        store_type = 'Flagship'
    WHERE store_id = 'S002';
    """
]


def main():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        for query in SOURCE_CHANGE_QUERIES:
            cursor.execute(query)

        connection.commit()
        print("Source system changes simulated successfully.")

    except Exception as error:
        print("Error while simulating source changes:", error)

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals():
            connection.close()


if __name__ == "__main__":
    main()