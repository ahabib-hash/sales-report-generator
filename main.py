import csv

MIN_TRANSACTION_VALUE = 50.0
SALES_FILE = "sales.csv"
REPORT_FILE = "report.csv"
ERROR_LOG_FILE = "errors.log"


def process_sales_file(filepath):
    summary = {}
    error_lines = []

    with open(filepath, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            # skip rows with the wrong number of columns
            if len(row) != 6:
                transaction_id = row[0] if row else "unknown"
                error_lines.append(f"SKIPPED [transaction_id={transaction_id}] reason=malformed row (expected 6 columns, got {len(row)})")
                continue

            transaction_id, transaction_date, product, region, quantity_str, unit_price_str = row
            # case-insensitive grouping key
            product = product.lower().strip()

            if not product:
                error_lines.append(f"SKIPPED [transaction_id={transaction_id}] reason=missing product name")
                continue

            if not quantity_str.strip():
                error_lines.append(f"SKIPPED [transaction_id={transaction_id}] reason=missing quantity")
                continue

            try:
                unit_price = float(unit_price_str)
            except ValueError:
                error_lines.append(f"SKIPPED [transaction_id={transaction_id}] reason=non-numeric unit_price ({unit_price_str})")
                continue

            try:
                quantity = int(quantity_str)
            except ValueError:
                error_lines.append(f"SKIPPED [transaction_id={transaction_id}] reason=non-numeric quantity ({quantity_str})")
                continue

            if quantity < 0:
                error_lines.append(f"SKIPPED [transaction_id={transaction_id}] reason=negative quantity ({quantity})")
                continue

            total_price = quantity * unit_price
            # ignore small transactions
            if total_price < MIN_TRANSACTION_VALUE:
                continue

            if product not in summary:
                summary[product] = {"revenue": 0.0, "units": 0, "orders": 0}

            summary[product]["revenue"] += total_price
            summary[product]["units"]   += quantity
            summary[product]["orders"]  += 1

    return summary, error_lines


def build_report_rows(summary):
    report_rows = []
    for product, data in summary.items():
        # avoid ZeroDivisionError if orders is ever 0
        avg_order_value = round(data["revenue"] / data["orders"], 2) if data["orders"] else 0.0
        report_rows.append({
            "product":         product,
            "total_revenue":   round(data["revenue"], 2),
            "total_units":     data["units"],
            "avg_order_value": avg_order_value,
        })

    report_rows.sort(key=lambda x: x["total_revenue"], reverse=True)
    return report_rows


try:
    summary, error_lines = process_sales_file(SALES_FILE)
except FileNotFoundError:
    print(f"Error: {SALES_FILE} not found")
    raise SystemExit(1)

report_rows = build_report_rows(summary)

try:
    with open(REPORT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["product", "total_revenue", "total_units", "avg_order_value"])
        writer.writeheader()
        writer.writerows(report_rows)

    with open(ERROR_LOG_FILE, "w") as f:
        f.write("\n".join(error_lines) + "\n" if error_lines else "")
except OSError as e:
    print(f"Error writing output files: {e}")
    raise SystemExit(1)
