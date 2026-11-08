import unittest

import config


class ConfigTests(unittest.TestCase):

    def test_prices(self):
        self.assertEqual(config.PRICES["consultation"], 35.0)
        self.assertEqual(config.PRICES["emergency visit"], 70.0)


if __name__ == "__main__":
    unittest.main()
