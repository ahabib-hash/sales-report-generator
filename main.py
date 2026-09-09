import csv

# storage
total_rows   = 0
skipped_rows = 0
summary      = {}
error_lines  = []

# task 1 - open and read sales.csv one row at a time
with open("sales.csv", "r", newline="") as f:
    reader = csv.reader(f)
    next(reader)  # skip the header

    for row in reader:
        total_rows += 1
        tid, date, product, region, qty_raw, price_raw = row

        # task 4 - skip bad rows and log them

        # skip if product name is empty
        if not product.strip():
            skipped_rows += 1
            error_lines.append(f"SKIPPED [transaction_id={tid}] reason=missing product name")
            continue

        # skip if quantity is empty
        if not qty_raw.strip():
            skipped_rows += 1
            error_lines.append(f"SKIPPED [transaction_id={tid}] reason=missing quantity")
            continue

        # skip if price is not a number
        try:
            price = float(price_raw)
        except ValueError:
            skipped_rows += 1
            error_lines.append(f"SKIPPED [transaction_id={tid}] reason=non-numeric unit_price ({price_raw})")
            continue

        # skip if quantity is not a number
        try:
            qty = int(qty_raw)
        except ValueError:
            skipped_rows += 1
            error_lines.append(f"SKIPPED [transaction_id={tid}] reason=non-numeric quantity ({qty_raw})")
            continue

        # skip if quantity is negative
        if qty < 0:
            skipped_rows += 1
            error_lines.append(f"SKIPPED [transaction_id={tid}] reason=negative quantity ({qty})")
            continue

        # task 2 - calculate total price and aggregate per product

        # total amount for this transaction
        total_price = qty * price

        # ignore small transactions
        if total_price < 50.0:
            continue

        # first time seeing this product — create its entry
        if product not in summary:
            summary[product] = {"revenue": 0.0, "units": 0, "orders": 0}

        # add to running totals
        summary[product]["revenue"] += total_price
        summary[product]["units"]   += qty
        summary[product]["orders"]  += 1

# task 3 - build and write report.csv

# one row per product with avg order value
report_rows = []
for product, data in summary.items():
    report_rows.append({
        "product":         product,
        "total_revenue":   round(data["revenue"], 2),
        "total_units":     data["units"],
        "avg_order_value": round(data["revenue"] / data["orders"], 2),
    })

# sort highest revenue first
report_rows.sort(key=lambda x: x["total_revenue"], reverse=True)

# write to file
with open("report.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["product", "total_revenue", "total_units", "avg_order_value"])
    writer.writeheader()
    writer.writerows(report_rows)

# task 4 - write all skipped rows to errors.log
with open("errors.log", "w") as f:
    f.write("\n".join(error_lines) + "\n")

# print final summary
print(f"Total rows read : {total_rows}")
print(f"Skipped rows    : {skipped_rows}")
print(f"\n{'Product':<12} {'Total Revenue':>15} {'Total Units':>12} {'Avg Order Value':>16}")
print("-" * 58)
for r in report_rows:
    print(f"{r['product']:<12} {r['total_revenue']:>15,.2f} {r['total_units']:>12} {r['avg_order_value']:>16,.2f}")