"""Task T05: sold out means having no units in any size."""
import unittest

import database
from stock import sold_out, sold_out_report


class T05Tests(unittest.TestCase):

    def test_with_some_size(self):
        stock = {"UR-5120": {"name": "City 3",
                             "units": {"S": 2, "M": 4, "L": 0}},
                 "EL-9050": {"name": "E-City 600",
                             "units": {"M": 0, "L": 0}}}
        self.assertEqual(sold_out(stock), ["EL-9050"])

    def test_sample_warehouse(self):
        self.assertEqual(sold_out(database.stock()), ["EL-9050"])

    def test_report(self):
        text = sold_out_report(database.stock(), "2026-10-13")
        self.assertNotIn("City 3", text)
        self.assertEqual(len(text.splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
