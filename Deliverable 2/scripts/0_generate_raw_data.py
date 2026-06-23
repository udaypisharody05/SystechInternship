import csv
import random
from datetime import date, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
CHANNELS = ["In-Store", "Online"]


def write_csv(batch_name, file_name, headers, rows):
    batch_dir = RAW_DIR / batch_name
    batch_dir.mkdir(parents=True, exist_ok=True)
    with open(batch_dir / file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def random_date(rng, start, end):
    return start + timedelta(days=rng.randint(0, (end - start).days))


def build_customers(start_id, count, rng):
    cities = [
        ("Bengaluru", "Karnataka"), ("Mumbai", "Maharashtra"),
        ("Delhi", "Delhi"), ("Chennai", "Tamil Nadu"),
        ("Hyderabad", "Telangana"), ("Kochi", "Kerala"),
        ("Pune", "Maharashtra"), ("Kolkata", "West Bengal"),
        ("Jaipur", "Rajasthan"), ("Ahmedabad", "Gujarat"),
    ]
    segments = ["Regular", "Premium", "Corporate"]
    rows = []
    for number in range(start_id, start_id + count):
        city, state = cities[(number - 1) % len(cities)]
        rows.append([
            f"CUST{number:03d}",
            f"Customer {number:03d}",
            f"customer{number:03d}@example.com",
            f"9{rng.randint(100000000, 999999999)}",
            city,
            state,
            rng.choice(segments),
            random_date(rng, date(2023, 1, 1), date(2025, 12, 31)),
            rng.randint(0, 5000),
        ])
    return rows


def build_products(rng):
    categories = [
        "Cricket", "Football", "Badminton", "Tennis", "Fitness",
        "Running", "Swimming", "Sportswear", "Accessories", "Cycling",
    ]
    brands = ["SG", "Adidas", "Yonex", "Wilson", "Decathlon"]
    rows = []
    for number in range(1, 51):
        unit_price = rng.randrange(399, 5000, 50)
        rows.append([
            f"PROD{number:03d}",
            f"Sports Product {number:03d}",
            categories[(number - 1) % len(categories)],
            brands[(number - 1) % len(brands)],
            unit_price,
            round(unit_price * 0.62, 2),
            f"Supplier {((number - 1) % 10) + 1:02d}",
            rng.randint(20, 250),
        ])
    return rows


def build_stores():
    locations = [
        ("Bengaluru", "Karnataka"), ("Mumbai", "Maharashtra"),
        ("Delhi", "Delhi"), ("Chennai", "Tamil Nadu"),
        ("Hyderabad", "Telangana"), ("Kochi", "Kerala"),
        ("Pune", "Maharashtra"), ("Kolkata", "West Bengal"),
        ("Jaipur", "Rajasthan"), ("Ahmedabad", "Gujarat"),
    ]
    return [
        [
            f"STORE{number:03d}",
            f"SportZone {city}",
            city,
            state,
            "Flagship" if number <= 3 else "Outlet",
            date(2021 + ((number - 1) % 4), ((number - 1) % 12) + 1, 1),
            f"Manager {number:02d}",
        ]
        for number, (city, state) in enumerate(locations, start=1)
    ]


def build_sales(start_id, count, customer_ids, rng, start_date, end_date):
    rows = []
    for number in range(start_id, start_id + count):
        rows.append([
            f"SALE{number:05d}",
            rng.choice(customer_ids),
            f"PROD{rng.randint(1, 50):03d}",
            f"STORE{rng.randint(1, 10):03d}",
            random_date(rng, start_date, end_date),
            rng.choices([1, 2, 3, 4, 5], weights=[45, 25, 15, 10, 5])[0],
            rng.choice([0, 5, 10, 15, 20]),
            rng.choice(PAYMENT_METHODS),
            rng.choices(CHANNELS, weights=[70, 30])[0],
        ])
    return rows


def main():
    rng = random.Random(42)
    customer_headers = [
        "customer_id", "customer_name", "email", "phone", "city", "state",
        "customer_segment", "signup_date", "loyalty_points",
    ]
    product_headers = [
        "product_id", "product_name", "category", "brand", "unit_price",
        "cost_price", "supplier", "stock_quantity",
    ]
    store_headers = [
        "store_id", "store_name", "city", "state", "store_type",
        "opening_date", "manager_name",
    ]
    sales_headers = [
        "sale_id", "customer_id", "product_id", "store_id", "sale_date",
        "quantity", "discount_percent", "payment_method", "channel",
    ]

    batch1_customers = build_customers(1, 100, rng)
    products = build_products(rng)
    stores = build_stores()
    batch1_sales = build_sales(
        1, 500, [row[0] for row in batch1_customers], rng,
        date(2026, 1, 1), date(2026, 6, 30),
    )

    new_customers = build_customers(101, 10, rng)
    changed_customer = list(batch1_customers[0])
    changed_customer[4] = "Mumbai"
    changed_customer[5] = "Maharashtra"
    changed_customer[6] = "Premium"
    changed_customer[8] = int(changed_customer[8]) + 750
    batch2_customers = [changed_customer] + new_customers
    batch2_sales = build_sales(
        501, 100,
        [f"CUST{number:03d}" for number in range(1, 111)],
        rng, date(2026, 7, 1), date(2026, 8, 31),
    )
    batch2_sales[0][1] = "CUST001"

    write_csv("batch_001", "customers.csv", customer_headers, batch1_customers)
    write_csv("batch_001", "products.csv", product_headers, products)
    write_csv("batch_001", "stores.csv", store_headers, stores)
    write_csv("batch_001", "sales.csv", sales_headers, batch1_sales)

    write_csv("batch_002", "customers.csv", customer_headers, batch2_customers)
    write_csv("batch_002", "products.csv", product_headers, [])
    write_csv("batch_002", "stores.csv", store_headers, [])
    write_csv("batch_002", "sales.csv", sales_headers, batch2_sales)

    print("Generated batch_001: 100 customers, 50 products, 10 stores, 500 sales")
    print("Generated batch_002: 1 changed customer, 10 new customers, 100 sales")


if __name__ == "__main__":
    main()
