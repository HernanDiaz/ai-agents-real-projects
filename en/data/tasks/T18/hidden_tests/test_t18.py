"""Task T18: one function to count days."""
import inspect
import unittest

import estimates
import orders
import returns


class T18Tests(unittest.TestCase):

    def test_no_copies(self):
        for module in (orders, returns, estimates):
            self.assertFalse(hasattr(module, "_days_between"), module.__name__)
            self.assertNotIn("fromisoformat", inspect.getsource(module),
                             module.__name__)

    def test_same_behavior(self):
        delivered = {"status": "delivered", "delivery_date": "2026-09-17"}
        self.assertTrue(returns.can_return(delivered, "2026-10-17"))
        self.assertFalse(returns.can_return(delivered, "2026-10-18"))
        order = {"payment": {"method": "transfer", "received": None},
                 "order_date": "2026-10-01"}
        self.assertFalse(orders.transfer_expired(order, "2026-10-06"))
        self.assertTrue(orders.transfer_expired(order, "2026-10-07"))
        self.assertTrue(estimates.free_tune_up(True, "2026-05-01", "2026-08-01"))
        self.assertFalse(estimates.free_tune_up(True, "2025-12-01", "2026-08-01"))


if __name__ == "__main__":
    unittest.main()
