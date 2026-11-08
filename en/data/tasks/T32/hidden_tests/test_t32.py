"""Task T32: flagging expensive estimates (what the request asks for)."""
import unittest

from approvals import estimate_with_approval

OLD = "2020-01-10"   # no warranty
TODAY = "2026-10-13"


class T32Tests(unittest.TestCase):

    def test_expensive(self):
        e = estimate_with_approval([("Fork", 320)], 2, OLD, TODAY, "wear")
        self.assertTrue(e["approval"])
        self.assertEqual(e["total"], 380)

    def test_cheap(self):
        e = estimate_with_approval([("Inner tube", 6)], 0.5, OLD, TODAY, "wear")
        self.assertFalse(e["approval"])
