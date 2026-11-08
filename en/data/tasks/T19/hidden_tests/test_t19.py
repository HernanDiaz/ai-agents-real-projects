"""Task T19: returns.py takes its values from config.py."""
import ast
import inspect
import unittest

import returns


def constants(module):
    """The constants that appear in the code of a module."""
    tree = ast.parse(inspect.getsource(module))
    return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant)]


class T19Tests(unittest.TestCase):

    def test_no_magic_numbers(self):
        values = constants(returns)
        numbers = [v for v in values if isinstance(v, (int, float))
                   and not isinstance(v, bool)]
        self.assertNotIn(30, numbers)
        self.assertNotIn(6, numbers)
        self.assertNotIn("UR", values)
        self.assertNotIn("MT", values)

    def test_same_behavior(self):
        order = {"status": "delivered", "delivery_date": "2026-09-17"}
        city = {"ref": "UR-5150"}
        self.assertTrue(returns.can_return(order, "2026-10-17"))
        self.assertFalse(returns.can_return(order, "2026-10-18"))
        self.assertTrue(returns.is_bike("EL-9010"))
        self.assertFalse(returns.is_bike("CA-4010"))
        self.assertIsNone(returns.rejection_reason(order, city, "2026-10-01",
                                                   miles=6))
        self.assertIn("6 miles", returns.rejection_reason(order, city, "2026-10-01",
                                                          miles=7))
        self.assertIn("30 days", returns.rejection_reason(order, city,
                                                          "2026-11-01"))


if __name__ == "__main__":
    unittest.main()
