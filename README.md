# Sales Report Generator

A small Python exercise that reads raw sales transactions from a CSV, cleans and aggregates them per product, and writes a summary report — while logging any rows it had to skip.

## What it does

`main.py` streams `sales.csv` row by row and:

- **Validates each row**, skipping (and logging to `errors.log`) any row with:
  - a missing product name
  - a missing quantity
  - a non-numeric unit price
  - a non-numeric or negative quantity
- **Aggregates** valid rows per product: total revenue, total units sold, and number of orders.
- **Filters out** transactions under $50 before aggregating.
- **Writes `report.csv`**, sorted by total revenue (highest first), with columns:
  `product, total_revenue, total_units, avg_order_value`
- Prints a run summary (rows read, rows skipped) and the report table to stdout.

## Files

| File | Purpose |
|---|---|
| `generate_data.py` | Generates a synthetic `sales.csv` (100,000 rows) with a mix of valid and intentionally malformed rows, for testing the pipeline. |
| `main.py` | Reads `sales.csv`, validates/aggregates, writes `report.csv` and `errors.log`. |

`sales.csv`, `report.csv`, and `errors.log` are generated at runtime and are not committed — see below.

## Usage

```bash
# 1. Generate sample input data
python3 generate_data.py

# 2. Run the report generator
python3 main.py
```

This produces `report.csv` (the aggregated report) and `errors.log` (skipped rows with reasons).
