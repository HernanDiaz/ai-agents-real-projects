"""Tarea T02: códigos postales que han perdido el cero inicial."""
import unittest

from envios import gastos_envio, zona


class PruebasT02(unittest.TestCase):

    def test_baleares_sin_cero(self):
        self.assertEqual(zona(7002), "baleares")
        self.assertEqual(zona("7002"), "baleares")
        self.assertEqual(zona(7800), "baleares")
        self.assertEqual(zona(" 07002 "), "baleares")

    def test_otras_zonas_como_numero(self):
        self.assertEqual(zona(38001), "canarias")
        self.assertEqual(zona(8001), "peninsula")
        self.assertEqual(zona(33001), "peninsula")

    def test_gastos(self):
        self.assertEqual(gastos_envio(45, 7002), 9.95)


if __name__ == "__main__":
    unittest.main()
