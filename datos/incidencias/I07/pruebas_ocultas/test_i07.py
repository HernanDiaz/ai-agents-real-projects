"""Incidencia I07: el formato de los euros, en un solo sitio."""
import unittest
from pathlib import Path

from facturas import texto_factura
from farmacia import etiqueta

FARMACIA = {"meloxicam": {"presentacion": "suspensión oral 1,5 mg/ml", "dosis_mg_kg": 0.1,
                          "especies": ["perro", "gato"], "existencias": 14, "precio": 1018.5}}
LOLA = {"nombre": "Lola", "especie": "perro", "peso_kg": 13.0, "alergias": []}
FACTURA = {"id": "F-0001", "dueno": "D-001", "fecha": "2026-10-16",
           "lineas": [{"concepto": "limpieza dental", "importe": 1120.0}]}


class PruebasI07(unittest.TestCase):

    def test_sin_copias(self):
        for archivo in ("farmacia.py", "facturas.py"):
            codigo = Path(archivo).read_text(encoding="utf-8")
            self.assertNotIn("def _euros", codigo)
            self.assertIn("formato_euros", codigo)

    def test_textos_iguales(self):
        self.assertIn("Precio: 1.018,50 €", etiqueta(FARMACIA, "meloxicam", LOLA))
        self.assertIn("1.120,00 €", texto_factura(FACTURA))
