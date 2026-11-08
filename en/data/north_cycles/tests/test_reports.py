"""Tests of the reports, with the sample database."""
import unittest

import database
from reports import (average_order, count_by_status, monthly_report, orders_of_month,
                     sales_by_category, total_sales)


class ReportsTests(unittest.TestCase):

    def setUp(self):
        self.orders = database.orders()

    def test_sales_without_canceled(self):
        october = orders_of_month(self.orders, 2026, 10)
        self.assertEqual(len(october), 8)
        self.assertEqual(total_sales(october), 2209.85)

    def test_average_order(self):
        self.assertEqual(average_order({}), 0)
        september = orders_of_month(self.orders, 2026, 9)
        self.assertEqual(average_order(september), 528.4)

    def test_categories(self):
        sales = sales_by_category(self.orders, database.catalog())
        self.assertEqual(next(iter(sales)), "e-bikes")

    def test_count(self):
        self.assertEqual(count_by_status(self.orders)["canceled"], 1)

    def test_report(self):
        self.assertIn("Report for 10/2026", monthly_report(2026, 10))


if __name__ == "__main__":
    unittest.main()
