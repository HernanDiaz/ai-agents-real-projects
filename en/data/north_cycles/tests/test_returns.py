"""Tests of the returns."""
import unittest

from returns import (can_return, pickup_cost, refund_amount, refund_deadline,
                     register_return, rejection_reason, return_summary)

TODAY = "2026-10-13"
CITY = {"ref": "UR-5150", "name": "City 5", "size": "M", "quantity": 1,
        "price": 589}
HELMET = {"ref": "CA-4010", "name": "City Helmet", "size": "M", "quantity": 1,
          "price": 49}
LIGHTS = {"ref": "LU-6080", "name": "City Light Kit", "size": "one size",
          "quantity": 1, "price": 25}


def order(lines, shipping=0, delivered="2026-09-17", status="delivered",
          zip_code="98101"):
    """A test order with the given lines."""
    return {"lines": lines, "shipping": shipping, "status": status,
            "delivery_date": delivered, "zip_code": zip_code}


class ReturnsTests(unittest.TestCase):

    def test_period(self):
        self.assertTrue(can_return(order([CITY]), TODAY))
        self.assertTrue(can_return(order([CITY]), "2026-10-17"))
        self.assertFalse(can_return(order([CITY]), "2026-10-18"))

    def test_not_delivered(self):
        self.assertFalse(can_return(order([CITY], status="shipped"), TODAY))

    def test_reasons(self):
        self.assertIsNone(rejection_reason(order([CITY]), CITY, TODAY, miles=2))
        self.assertIn("miles", rejection_reason(order([CITY]), CITY, TODAY,
                                                miles=15))
        shorts = {"ref": "RO-2050", "name": "Pro Bib Shorts", "size": "M",
                  "quantity": 1, "price": 79}
        self.assertIn("hygiene", rejection_reason(order([shorts]), shorts, TODAY,
                                                  unsealed=True))

    def test_partial_refund(self):
        o = order([HELMET, LIGHTS], shipping=4.95)
        self.assertEqual(refund_amount(o, [{"ref": "CA-4010", "quantity": 1}]), 49)

    def test_full_refund(self):
        o = order([HELMET, LIGHTS], shipping=4.95)
        returned = [{"ref": "CA-4010", "quantity": 1},
                    {"ref": "LU-6080", "quantity": 1}]
        self.assertEqual(refund_amount(o, returned), 78.95)

    def test_pickup(self):
        self.assertEqual(pickup_cost(order([HELMET])), 0)
        self.assertEqual(pickup_cost(order([HELMET], zip_code="96813")), 14.95)

    def test_refund_within_14_days(self):
        self.assertEqual(refund_deadline("2026-10-20"), "2026-11-03")

    def test_register(self):
        stock = {"CA-4010": {"name": "City Helmet", "units": {"M": 0}}}
        o = order([HELMET])
        register_return(o, [{"ref": "CA-4010", "quantity": 1}], TODAY, stock)
        self.assertEqual(o["status"], "return in progress")
        self.assertEqual(stock["CA-4010"]["units"]["M"], 1)

    def test_summary(self):
        o = order([CITY])
        returned = [{"ref": "UR-5150", "quantity": 1}]
        self.assertEqual(
            return_summary("NC-10482", o, returned, TODAY),
            "Return of order NC-10482 accepted: $589.00 will be refunded.")
        self.assertEqual(return_summary("NC-10482", o, returned, "2026-11-30"),
                         "Order NC-10482 cannot be returned.")


if __name__ == "__main__":
    unittest.main()
