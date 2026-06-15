import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)


CUSTOMER_FIRST_NAMES = [
    "Rahul", "Ananya", "Arjun", "Priya", "Vikram", "Neha", "Aman", "Diya", "Karan", "Sneha",
    "Rohan", "Meera", "Aditya", "Isha", "Nikhil", "Tanvi", "Varun", "Pooja", "Siddharth", "Aditi",
    "Manav", "Kavya", "Harsh", "Riya", "Yash", "Naina", "Dev", "Sanya", "Aryan", "Tara",
    "Kabir", "Avni", "Ishan", "Mira", "Rudra", "Kiara", "Neil", "Anika", "Reyansh", "Myra",
    "Sameer", "Shruti", "Akash", "Lavanya", "Gaurav", "Mitali", "Rakesh", "Divya", "Sahil", "Nisha"
]

LAST_NAMES = [
    "Sharma", "Nair", "Mehta", "Iyer", "Singh", "Reddy", "Verma", "Menon", "Kapoor", "Das",
    "Patel", "Rao", "Gupta", "Joshi", "Khan", "Bose", "Chopra", "Pillai", "Mishra", "Shetty"
]

CITIES = [
    ("Bengaluru", "Karnataka"),
    ("Mumbai", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Chennai", "Tamil Nadu"),
    ("Hyderabad", "Telangana"),
    ("Kochi", "Kerala"),
    ("Pune", "Maharashtra"),
    ("Kolkata", "West Bengal"),
    ("Jaipur", "Rajasthan"),
    ("Ahmedabad", "Gujarat")
]

PRODUCTS = [
    ("Cricket Bat", "Cricket", "SG", 2499, 1550, "SportLine Distributors"),
    ("Cricket Ball Pack", "Cricket", "Kookaburra", 599, 320, "Elite Sports Supply"),
    ("Batting Gloves", "Cricket", "SS", 1299, 700, "ProGear Wholesale"),
    ("Football", "Football", "Nivia", 899, 470, "SportLine Distributors"),
    ("Football Studs", "Football", "Adidas", 3499, 2300, "Urban Sports Co"),
    ("Goalkeeper Gloves", "Football", "Puma", 1499, 850, "Elite Sports Supply"),
    ("Badminton Racket", "Badminton", "Yonex", 1799, 980, "ShuttlePro Traders"),
    ("Shuttlecock Tube", "Badminton", "Li-Ning", 749, 410, "ShuttlePro Traders"),
    ("Badminton Shoes", "Badminton", "Yonex", 2999, 1900, "Urban Sports Co"),
    ("Tennis Racket", "Tennis", "Wilson", 3499, 2300, "CourtKing Suppliers"),
    ("Tennis Ball Can", "Tennis", "Head", 499, 250, "CourtKing Suppliers"),
    ("Tennis Shoes", "Tennis", "Nike", 4299, 2900, "Urban Sports Co"),
    ("Basketball", "Basketball", "Spalding", 1299, 760, "Elite Sports Supply"),
    ("Basketball Shoes", "Basketball", "Nike", 4999, 3300, "Urban Sports Co"),
    ("Skipping Rope", "Fitness", "Decathlon", 399, 180, "FitMax Wholesale"),
    ("Dumbbell Set", "Fitness", "Domyos", 2999, 1900, "FitMax Wholesale"),
    ("Yoga Mat", "Fitness", "Boldfit", 799, 420, "FitMax Wholesale"),
    ("Gym Gloves", "Fitness", "Decathlon", 499, 220, "FitMax Wholesale"),
    ("Resistance Band", "Fitness", "Boldfit", 699, 320, "FitMax Wholesale"),
    ("Running Shoes", "Running", "Adidas", 3999, 2600, "Urban Sports Co"),
    ("Running Shorts", "Running", "Puma", 999, 480, "ActiveWear Hub"),
    ("Sports T-Shirt", "Sportswear", "Puma", 699, 310, "ActiveWear Hub"),
    ("Track Pants", "Sportswear", "Nike", 1599, 850, "ActiveWear Hub"),
    ("Sports Jacket", "Sportswear", "Adidas", 2999, 1750, "ActiveWear Hub"),
    ("Swimming Goggles", "Swimming", "Speedo", 799, 390, "AquaSport Traders"),
    ("Swimming Cap", "Swimming", "Speedo", 399, 170, "AquaSport Traders"),
    ("Kickboard", "Swimming", "Decathlon", 999, 540, "AquaSport Traders"),
    ("Table Tennis Paddle", "Table Tennis", "Stag", 999, 520, "Indoor Sports Supply"),
    ("Table Tennis Balls", "Table Tennis", "Stag", 299, 120, "Indoor Sports Supply"),
    ("TT Table Net", "Table Tennis", "Stag", 699, 310, "Indoor Sports Supply"),
    ("Hockey Stick", "Hockey", "Cosco", 1499, 820, "Elite Sports Supply"),
    ("Hockey Ball", "Hockey", "Nivia", 349, 150, "Elite Sports Supply"),
    ("Boxing Gloves", "Combat Sports", "USI", 1999, 1100, "ProGear Wholesale"),
    ("Punching Bag", "Combat Sports", "USI", 4499, 3100, "ProGear Wholesale"),
    ("Cycling Helmet", "Cycling", "Btwin", 1599, 850, "CyclePro Suppliers"),
    ("Cycling Gloves", "Cycling", "Btwin", 699, 300, "CyclePro Suppliers"),
    ("Water Bottle", "Accessories", "Nike", 499, 190, "ActiveWear Hub"),
    ("Sports Bag", "Accessories", "Puma", 1499, 790, "ActiveWear Hub"),
    ("Wrist Band", "Accessories", "Nivia", 199, 70, "SportLine Distributors"),
    ("Ankle Support", "Accessories", "Boldfit", 599, 260, "FitMax Wholesale")
]


def random_date(start_date, end_date):
    days_between = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days_between))


def write_csv(file_name, headers, rows):
    file_path = RAW_DATA_DIR / file_name

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Created {file_path}")


def generate_customers():
    rows = []

    for i in range(1, 51):
        first_name = CUSTOMER_FIRST_NAMES[i - 1]
        last_name = random.choice(LAST_NAMES)
        city, state = random.choice(CITIES)

        customer_id = f"C{i:03d}"
        customer_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
        phone = f"9{random.randint(100000000, 999999999)}"
        segment = random.choices(
            ["Regular", "Premium", "Corporate"],
            weights=[60, 30, 10]
        )[0]
        signup_date = random_date(datetime(2024, 1, 1), datetime(2026, 5, 31)).date()
        loyalty_points = random.randint(0, 5000)

        rows.append([
            customer_id, customer_name, email, phone, city, state,
            segment, signup_date, loyalty_points
        ])

    return rows


def generate_products():
    rows = []

    for i, product in enumerate(PRODUCTS, start=1):
        product_name, category, brand, unit_price, cost_price, supplier = product
        product_id = f"P{i:03d}"
        stock_quantity = random.randint(20, 250)

        rows.append([
            product_id, product_name, category, brand, unit_price,
            cost_price, supplier, stock_quantity
        ])

    return rows


def generate_stores():
    store_names = [
        "SportZone Bengaluru", "SportZone Mumbai", "SportZone Delhi",
        "SportZone Chennai", "SportZone Hyderabad", "SportZone Kochi",
        "SportZone Pune", "SportZone Kolkata", "SportZone Jaipur",
        "SportZone Ahmedabad"
    ]

    managers = [
        "Amit Rao", "Suresh Menon", "Karthik Iyer", "Raj Malhotra", "Farhan Khan",
        "Deepak Nair", "Vivek Gupta", "Sanjay Bose", "Arvind Patel", "Nitin Joshi"
    ]

    rows = []

    for i, ((city, state), store_name, manager) in enumerate(zip(CITIES, store_names, managers), start=1):
        store_id = f"S{i:03d}"
        store_type = "Flagship" if city in ["Bengaluru", "Mumbai", "Delhi"] else "Outlet"
        opening_date = random_date(datetime(2021, 1, 1), datetime(2025, 12, 31)).date()

        rows.append([
            store_id, store_name, city, state, store_type, opening_date, manager
        ])

    return rows


def generate_sales(customers, products, stores):
    rows = []
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 6, 15)

    payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
    channels = ["In-Store", "Online"]

    for i in range(1, 201):
        sale_id = f"SA{i:04d}"

        customer_id = random.choice(customers)[0]
        product = random.choice(products)
        product_id = product[0]
        store_id = random.choice(stores)[0]

        sale_date = random_date(start_date, end_date).date()
        quantity = random.choices([1, 2, 3, 4, 5], weights=[45, 25, 15, 10, 5])[0]
        discount_percent = random.choices([0, 5, 10, 15, 20], weights=[40, 25, 20, 10, 5])[0]
        payment_method = random.choice(payment_methods)
        channel = random.choices(channels, weights=[70, 30])[0]

        rows.append([
            sale_id, customer_id, product_id, store_id, sale_date,
            quantity, discount_percent, payment_method, channel
        ])

    return rows


def main():
    customers = generate_customers()
    products = generate_products()
    stores = generate_stores()
    sales = generate_sales(customers, products, stores)

    write_csv(
        "customers.csv",
        [
            "customer_id", "customer_name", "email", "phone", "city", "state",
            "customer_segment", "signup_date", "loyalty_points"
        ],
        customers
    )

    write_csv(
        "products.csv",
        [
            "product_id", "product_name", "category", "brand", "unit_price",
            "cost_price", "supplier", "stock_quantity"
        ],
        products
    )

    write_csv(
        "stores.csv",
        [
            "store_id", "store_name", "city", "state", "store_type",
            "opening_date", "manager_name"
        ],
        stores
    )

    write_csv(
        "sales.csv",
        [
            "sale_id", "customer_id", "product_id", "store_id", "sale_date",
            "quantity", "discount_percent", "payment_method", "channel"
        ],
        sales
    )

    print("Raw data generation completed successfully.")


if __name__ == "__main__":
    main()