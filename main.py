import csv

MIN_TRANSACTION_VALUE = 50.0
SALES_FILE = "sales.csv"
REPORT_FILE = "report.csv"
ERROR_LOG_FILE = "errors.log"


def process_sales_file(filepath, error_log_path):
    summary = {}

    with open(filepath, "r", newline="") as f, \
         open(error_log_path, "w") as err_f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            if len(row) != 6:
                transaction_id = row[0] if row else "unknown"
                err_f.write(f"SKIPPED [transaction_id={transaction_id}] reason=malformed row (expected 6 columns, got {len(row)})\n")
                continue

            transaction_id, transaction_date, product, region, quantity_str, unit_price_str = row
            product = product.lower().strip()

            reasons = []

            if not product:
                reasons.append("missing product name")

            quantity = None
            if not quantity_str.strip():
                reasons.append("missing quantity")
            else:
                try:
                    quantity = int(quantity_str)
                    if quantity < 0:
                        reasons.append(f"negative quantity ({quantity})")
                except ValueError:
                    reasons.append(f"non-numeric quantity ({quantity_str})")

            unit_price = None
            try:
                unit_price = float(unit_price_str)
            except ValueError:
                reasons.append(f"non-numeric unit_price ({unit_price_str})")

            if reasons:
                err_f.write(f"SKIPPED [transaction_id={transaction_id}] reasons={', '.join(reasons)}\n")
                continue

            total_price = quantity * unit_price
            if total_price < MIN_TRANSACTION_VALUE:
                continue

            if product not in summary:
                summary[product] = {"revenue": 0.0, "units": 0, "orders": 0}

            summary[product]["revenue"] += total_price
            summary[product]["units"]   += quantity
            summary[product]["orders"]  += 1

    return summary


def build_report_rows(summary):
    report_rows = []
    for product, data in summary.items():
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
    summary = process_sales_file(SALES_FILE, ERROR_LOG_FILE)
except FileNotFoundError:
    print(f"Error: {SALES_FILE} not found")
    raise SystemExit(1)

report_rows = build_report_rows(summary)

try:
    with open(REPORT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["product", "total_revenue", "total_units", "avg_order_value"])
        writer.writeheader()
        writer.writerows(report_rows)
except OSError as e:
    print(f"Error writing output files: {e}")
    raise SystemExit(1)