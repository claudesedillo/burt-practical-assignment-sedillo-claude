import json
import csv
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise RuntimeError(f"Input file not found: {path}")
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Invalid JSON in {path}: {error}")

def read_transactions():
    return read_json(DATA_DIR / "transactions.json")

def read_stores():
    return read_json(DATA_DIR / "stores.json")

def parse_revenue(revenue):
    if revenue is None:
        return Decimal("0")

    cleaned_revenue = re.sub(r"[^\d.-]", "", str(revenue))

    try:
        return Decimal(cleaned_revenue)
    except InvalidOperation:
        return Decimal("0")

def build_store_lookup(store_list):
    return {
        store["shop_id"]: store
        for store in store_list
        if store.get("shop_id")
    }

def build_transaction_report(transaction_list, stores_with_id):
    transaction_report = []

    for transaction in transaction_list:
        shop_id = transaction.get("shop_id")
        store = stores_with_id.get(shop_id, {})

        row = {
            "date": transaction.get("date") or "N/A",
            "country": transaction.get("country") or "N/A",
            "channel": transaction.get("channel") or "N/A",
            "category": transaction.get("category") or "N/A",
            "shop_name": store.get("name") or "N/A",
            "shop_city": store.get("city") or "N/A",
            "units_sold": transaction.get("units_sold", "N/A"),
            "revenue": transaction.get("revenue") or "N/A",
            "transactions": transaction.get("transactions", "N/A")
        }

        transaction_report.append(row)

    return transaction_report

def build_store_summary(transaction_list, store_list):
    store_summary = {}

    for index, store in enumerate(store_list):
        shop_id = store.get("shop_id")

        if shop_id:
            summary_key = shop_id
        else:
            summary_key = f"missing_store_{index}"

        store_summary[summary_key] = {
            "shop_name": store.get("name") or "N/A",
            "shop_city": store.get("city") or "N/A",
            "total_units_sold": 0,
            "total_revenue": Decimal("0"),
            "total_transactions": 0
        }

    for transaction in transaction_list:
        shop_id = transaction.get("shop_id")

        if shop_id not in store_summary:
            store_summary[shop_id] = {
                "shop_name": "N/A",
                "shop_city": "N/A",
                "total_units_sold": 0,
                "total_revenue": Decimal("0"),
                "total_transactions": 0
            }

        summary = store_summary[shop_id]

        summary["total_units_sold"] += transaction.get("units_sold") or 0
        summary["total_revenue"] += parse_revenue(transaction.get("revenue"))
        summary["total_transactions"] += transaction.get("transactions") or 0

    return store_summary

def write_transaction_report(transaction_report):
    column_names = [
        "date",
        "country",
        "channel",
        "category",
        "shop_name",
        "shop_city",
        "units_sold",
        "revenue",
        "transactions"
    ]

    with open(REPORTS_DIR / "transaction_report.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=column_names)

        writer.writeheader()
        writer.writerows(transaction_report)

def write_store_summary(store_summary):
    column_names = [
        "shop_name",
        "shop_city",
        "total_units_sold",
        "total_revenue",
        "total_transactions"
    ]

    with open(REPORTS_DIR / "store_summary.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=column_names)

        writer.writeheader()

        for summary in store_summary.values():
            row = summary.copy()
            row["total_revenue"] = f"{row['total_revenue']:.2f}"
            writer.writerow(row)

def main():
    try:
        transaction_list = read_transactions()
        store_list = read_stores()
        stores_with_id = build_store_lookup(store_list)

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        transaction_report = build_transaction_report(transaction_list,stores_with_id)
        write_transaction_report(transaction_report)

        store_summary = build_store_summary(transaction_list, store_list)
        write_store_summary(store_summary)
    except RuntimeError as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()
