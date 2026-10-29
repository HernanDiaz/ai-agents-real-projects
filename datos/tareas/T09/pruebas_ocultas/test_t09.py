"""Tarea T09: cuotas del pago a plazos y su línea en la factura."""
import unittest

from facturas import factura, texto_factura
from pedidos import cuotas

LINEA = {"ref": "CR-7010", "nombre": "Aero 3", "talla": "54", "cantidad": 1,
         "precio": 1150}


class PruebasT09(unittest.TestCase):

    def test_cuotas(self):
        self.assertEqual(cuotas(1000, 3), [333.33, 333.33, 333.34])
        self.assertEqual(cuotas(1150, 6), [191.67] * 5 + [191.65])
        self.assertEqual(len(cuotas(301, 12)), 12)

    def test_suman_el_importe(self):
        for importe in (301, 449.95, 1649, 3490):
            for meses in (3, 6, 12):
                self.assertEqual(round(sum(cuotas(importe, meses)), 2), importe)

    def test_errores(self):
        with self.assertRaises(ValueError):
            cuotas(300, 3)
        with self.assertRaises(ValueError):
            cuotas(1000, 4)

    def test_factura(self):
        pedido = {"lineas": [LINEA], "envio": 0, "importe": 1150,
                  "pago": {"forma": "tarjeta", "recibido": "2026-09-08", "plazos": 6}}
        texto = texto_factura(factura("F2026-0002", "CN-11020", pedido,
                                      {"nombre": "Marta Iglesias"}, "2026-09-08"))
        self.assertIn("Pago aplazado: 6 cuotas de 191,67 €", texto)
        pedido["pago"] = {"forma": "tarjeta", "recibido": "2026-09-08"}
        texto = texto_factura(factura("F2026-0002", "CN-11020", pedido,
                                      {"nombre": "Marta Iglesias"}, "2026-09-08"))
        self.assertNotIn("Pago aplazado", texto)


if __name__ == "__main__":
    unittest.main()
