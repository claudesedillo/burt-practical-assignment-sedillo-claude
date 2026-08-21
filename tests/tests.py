import unittest
from decimal import Decimal

from src.run import (
    parse_revenue,
    build_store_lookup,
    build_transaction_report,
    build_store_summary
)


class TestSalesReports(unittest.TestCase):

    def test_parse_revenue(self):
        self.assertEqual(parse_revenue("123.45"), Decimal("123.45"))
        self.assertEqual(parse_revenue("1,234.50"), Decimal("1234.50"))
        self.assertEqual(parse_revenue("$25.00"), Decimal("25.00"))
        self.assertEqual(parse_revenue(None), Decimal("0"))

    def test_build_store_lookup_ignores_store_without_id(self):
        store_list = [
            {
                "shop_id": "S100",
                "name": "Downtown Flagship",
                "city": "San Francisco"
            },
            {
                "name": "Mystery Shop",
                "city": "Manila"
            }
        ]

        stores_with_id = build_store_lookup(store_list)

        self.assertIn("S100", stores_with_id)
        self.assertEqual(len(stores_with_id), 1)

    def test_transaction_report_uses_na_for_unknown_store(self):
        transaction_list = [
            {
                "date": "2024-03-01",
                "country": "",
                "channel": "online",
                "category": "home",
                "shop_id": "S999",
                "units_sold": 10,
                "revenue": "9.99",
                "transactions": 8
            }
        ]

        stores_with_id = {}

        report = build_transaction_report(
            transaction_list,
            stores_with_id
        )

        self.assertEqual(report[0]["country"], "N/A")
        self.assertEqual(report[0]["shop_name"], "N/A")
        self.assertEqual(report[0]["shop_city"], "N/A")

    def test_store_summary_aggregates_transactions(self):
        store_list = [
            {
                "shop_id": "S100",
                "name": "Downtown Flagship",
                "city": "San Francisco"
            }
        ]

        transaction_list = [
            {
                "shop_id": "S100",
                "units_sold": 10,
                "revenue": "20.50",
                "transactions": 5
            },
            {
                "shop_id": "S100",
                "units_sold": 15,
                "revenue": "$30.25",
                "transactions": 7
            }
        ]

        summary = build_store_summary(
            transaction_list,
            store_list
        )

        self.assertEqual(summary["S100"]["total_units_sold"], 25)
        self.assertEqual(
            summary["S100"]["total_revenue"],
            Decimal("50.75")
        )
        self.assertEqual(summary["S100"]["total_transactions"], 12)


if __name__ == "__main__":
    unittest.main()
