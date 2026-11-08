"""Incident I08: what an owner has paid."""
import unittest

from invoices import owner_total

INVOICES = [{"id": "INV-1", "owner": "C-001", "date": "2026-10-01",
             "lines": [{"item": "consultation", "amount": 35.0}]},
            {"id": "INV-2", "owner": "C-001", "date": "2026-10-15",
             "lines": [{"item": "wound care", "amount": 22.1},
                       {"item": "deworming", "amount": 15.05}]},
            {"id": "INV-3", "owner": "C-002", "date": "2026-10-10",
             "lines": [{"item": "wound care", "amount": 22.0}]},
            {"id": "INV-4", "owner": "C-001", "date": "2026-11-02",
             "lines": [{"item": "consultation", "amount": 35.0}]}]


class I08Tests(unittest.TestCase):

    def test_period(self):
        self.assertEqual(owner_total(INVOICES, "C-001", "2026-10-01", "2026-10-15"),
                         72.15)
        self.assertEqual(owner_total(INVOICES, "C-001", "2026-10-02", "2026-10-31"),
                         37.15)

    def test_empty(self):
        self.assertEqual(owner_total(INVOICES, "C-003", "2026-01-01", "2026-12-31"), 0)
