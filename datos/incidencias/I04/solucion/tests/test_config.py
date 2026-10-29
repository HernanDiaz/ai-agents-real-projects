import unittest

import config


class PruebasConfig(unittest.TestCase):

    def test_tarifas(self):
        self.assertEqual(config.TARIFAS["consulta"], 35.0)
        self.assertEqual(config.TARIFAS["urgencia"], 70.0)


if __name__ == "__main__":
    unittest.main()
