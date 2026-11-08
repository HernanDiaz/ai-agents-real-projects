"""Task T35: management's decisions about the loyalty discount."""
import unittest

from loyalty import loyalty_discount

TODAY = "2026-10-24"


def order(status, date):
    return {"customer": "CL-0001", "status": status, "amount": 80,
            "order_date": date, "delivery_date": date}


THREE = {f"NC-{n}": order("delivered", f"2026-0{n}-10") for n in (3, 5, 7)}


class T35CriterionTests(unittest.TestCase):

    def test_percentage_and_cap(self):
        self.assertEqual(loyalty_discount(THREE, "CL-0001", 200, TODAY), 10)
        self.assertEqual(loyalty_discount(THREE, "CL-0001", 1000, TODAY), 25)
        self.assertEqual(loyalty_discount(THREE, "CL-0001", 100, TODAY), 0)

    def test_only_the_last_year(self):
        old = {f"NC-{n}": order("delivered", f"2024-0{n}-10") for n in (3, 5, 7)}
        self.assertEqual(loyalty_discount(old, "CL-0001", 200, TODAY), 0)
        two = {k: v for k, v in THREE.items() if k != "NC-7"}
        self.assertEqual(loyalty_discount(two, "CL-0001", 200, TODAY), 0)

    def test_return_in_progress(self):
        with_return = dict(THREE, **{"NC-9": order("return in progress", "2026-09-20")})
        self.assertEqual(loyalty_discount(with_return, "CL-0001", 200, TODAY), 0)
