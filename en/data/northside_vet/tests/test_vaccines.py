import unittest

from vaccines import overdue, pending_notices, upcoming

LOLA = [{"vaccine": "rabies", "last": "2025-08-22", "next": "2026-08-22"},
        {"vaccine": "leptospirosis", "last": "2025-11-12", "next": "2026-11-12"},
        {"vaccine": "DHPP", "last": "2026-03-01", "next": "2027-03-01"}]


class VaccinesTests(unittest.TestCase):

    def test_overdue(self):
        self.assertEqual(overdue(LOLA, "2026-10-20"), ["rabies"])

    def test_upcoming(self):
        self.assertEqual(upcoming(LOLA, "2026-10-20"), ["leptospirosis"])
        self.assertEqual(upcoming(LOLA, "2026-10-20", days=10), [])

    def test_notices(self):
        self.assertEqual(pending_notices({"P-001": LOLA}, "2026-10-20"),
                         {"P-001": ["rabies", "leptospirosis"]})


if __name__ == "__main__":
    unittest.main()
