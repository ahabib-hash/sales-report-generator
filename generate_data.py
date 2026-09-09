# generate_data.py
import csv, random, uuid
from datetime import date, timedelta

products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headset"]
regions = ["North", "South", "East", "West"]
prices = {"Laptop": 999.99, "Mouse": 29.99, "Keyboard": 79.99, "Monitor": 349.99, "Headset": 89.99}

with open("sales.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["transaction_id", "date", "product", "region", "quantity", "unit_price"])
    
    start = date(2024, 1, 1)
    bad_indices = set(random.sample(range(100_000), 500))

    for i in range(100_000):
        d = start + timedelta(days=random.randint(0, 364))
        product = random.choice(products)
        price = prices[product]

        if i in bad_indices:
            bad_type = random.choice(["missing_product", "negative_qty", "non_numeric_price", "missing_qty"])

            if bad_type == "missing_product":
                writer.writerow([str(uuid.uuid4()), d, "", random.choice(regions), random.randint(1, 5), price])

            elif bad_type == "negative_qty":
                random_neg_qty = random.randint(-10, -1)
                writer.writerow([str(uuid.uuid4()), d, product, random.choice(regions), random_neg_qty, price])

            elif bad_type == "non_numeric_price":
                writer.writerow([str(uuid.uuid4()), d, product, random.choice(regions), random.randint(1, 5), "N/A"])

            elif bad_type == "missing_qty":
                writer.writerow([str(uuid.uuid4()), d, product, random.choice(regions), "", price])
        else:
            writer.writerow([str(uuid.uuid4()), d, product, random.choice(regions), random.randint(1, 5), price])

print("sales.csv generated!")