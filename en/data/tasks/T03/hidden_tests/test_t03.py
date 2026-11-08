"""Task T03: shipping is only refunded if the whole order is returned."""
import unittest

from returns import refund_amount

HELMETS = {"ref": "CA-4100", "name": "Trail Helmet", "size": "L", "quantity": 2,
           "price": 89}
LIGHTS = {"ref": "LU-6080", "name": "City Light Kit", "size": "one size",
          "quantity": 2, "price": 25}


def order(lines, shipping):
    """A delivered order with the given lines."""
    return {"lines": lines, "shipping": shipping, "status": "delivered",
            "delivery_date": "2026-10-01", "zip_code": "00907"}


class T03Tests(unittest.TestCase):

    def test_one_of_two_units(self):
        o = order([HELMETS], 9.95)
        self.assertEqual(refund_amount(o, [{"ref": "CA-4100", "quantity": 1}]), 89)

    def test_all_units(self):
        o = order([HELMETS], 9.95)
        self.assertEqual(refund_amount(o, [{"ref": "CA-4100", "quantity": 2}]),
                         187.95)

    def test_in_several_entries(self):
        o = order([HELMETS], 9.95)
        returned = [{"ref": "CA-4100", "quantity": 1},
                    {"ref": "CA-4100", "quantity": 1}]
        self.assertEqual(refund_amount(o, returned), 187.95)

    def test_two_lines_halfway(self):
        o = order([HELMETS, LIGHTS], 4.95)
        returned = [{"ref": "CA-4100", "quantity": 1},
                    {"ref": "LU-6080", "quantity": 1}]
        self.assertEqual(refund_amount(o, returned), 114)


if __name__ == "__main__":
    unittest.main()
