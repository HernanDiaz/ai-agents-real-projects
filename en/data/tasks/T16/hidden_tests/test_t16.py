"""Task T16: return period extended for the holidays."""
import unittest

from notices import delivery_notice
from returns import can_return

LAURA = {"name": "Laura Green"}


def delivered(date):
    """An order delivered on the given date."""
    return {"status": "delivered", "delivery_date": date, "lines": [], "shipping": 0,
            "zip_code": "97205"}


class T16Tests(unittest.TestCase):

    def test_campaign(self):
        self.assertTrue(can_return(delivered("2026-12-10"), "2027-01-25"))
        self.assertTrue(can_return(delivered("2026-12-10"), "2027-01-31"))
        self.assertFalse(can_return(delivered("2026-12-10"), "2027-02-01"))
        self.assertTrue(can_return(delivered("2026-11-15"), "2027-01-31"))
        self.assertTrue(can_return(delivered("2026-12-28"), "2027-01-30"))

    def test_outside_campaign(self):
        self.assertTrue(can_return(delivered("2026-11-14"), "2026-12-14"))
        self.assertFalse(can_return(delivered("2026-11-14"), "2026-12-15"))
        self.assertTrue(can_return(delivered("2027-01-05"), "2027-02-04"))
        self.assertFalse(can_return(delivered("2027-01-05"), "2027-02-05"))

    def test_notice(self):
        text = delivery_notice("NC-11600", {"delivery_date": "2026-11-20"}, LAURA)
        self.assertIn("until 01/31/2027", text)
        text = delivery_notice("NC-10482", {"delivery_date": "2026-09-17"}, LAURA)
        self.assertIn("until 10/17/2026", text)


if __name__ == "__main__":
    unittest.main()
