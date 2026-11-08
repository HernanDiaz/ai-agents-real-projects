"""Task T06: paid bank transfers do not expire."""
import unittest

import database
import orders

HELMET = {"ref": "CA-4010", "name": "City Helmet", "size": "M", "quantity": 1,
          "price": 49}


class T06Tests(unittest.TestCase):

    def test_paid_does_not_expire(self):
        paid = orders.create_order("CL-0011", [HELMET], "97204", "transfer",
                                   "2026-10-01")
        orders.record_payment(paid, "2026-10-03")
        unpaid = orders.create_order("CL-0001", [HELMET], "98101", "transfer",
                                     "2026-10-01")
        self.assertFalse(orders.transfer_expired(paid, "2026-10-13"))
        everything = {"NC-A": paid, "NC-B": unpaid}
        self.assertEqual(orders.expire_transfers(everything, "2026-10-13"), ["NC-B"])
        self.assertEqual(paid["status"], "processing")

    def test_sample_database(self):
        everything = database.orders()
        self.assertEqual(orders.expire_transfers(everything, "2026-10-13"),
                         ["NC-11460"])


if __name__ == "__main__":
    unittest.main()
