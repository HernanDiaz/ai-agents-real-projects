"""Pruebas de los pedidos: alta, cancelación, envíos y transferencias."""
import unittest

import pedidos

CASCO = {"ref": "CA-4010", "nombre": "Casco Ciudad", "talla": "M", "cantidad": 1,
         "precio": 49}
LUCES = {"ref": "LU-6080", "nombre": "Kit Luces Ciudad", "talla": "única",
         "cantidad": 2, "precio": 25}


def nuevo(lineas, forma_pago="tarjeta", hoy="2026-10-13"):
    """Un pedido de prueba con destino a Oviedo."""
    return pedidos.crear_pedido("CL-0001", lineas, "33001", forma_pago, hoy)


class PruebasPedidos(unittest.TestCase):

    def test_subtotal(self):
        self.assertEqual(pedidos.subtotal([CASCO, LUCES]), 99)

    def test_crear_con_tarjeta(self):
        pedido = nuevo([CASCO])
        self.assertEqual(pedido["envio"], 4.95)
        self.assertEqual(pedido["importe"], 53.95)
        self.assertEqual(pedido["estado"], "en preparación")

    def test_crear_con_transferencia(self):
        pedido = nuevo([CASCO, LUCES], "transferencia")
        self.assertEqual(pedido["estado"], "pendiente de pago")
        self.assertIsNone(pedido["pago"]["recibido"])

    def test_errores_al_crear(self):
        with self.assertRaises(ValueError):
            nuevo([])
        with self.assertRaises(ValueError):
            nuevo([CASCO], "cheque")

    def test_siguiente_numero(self):
        self.assertEqual(pedidos.siguiente_numero({"CN-10482": {}, "CN-11460": {}}),
                         "CN-11461")

    def test_cancelar(self):
        pedido = nuevo([CASCO])
        pedidos.cancelar(pedido, "cancelado por el cliente", "2026-10-13")
        self.assertEqual(pedido["estado"], "cancelado")
        with self.assertRaises(ValueError):
            pedidos.cancelar(pedido, "otra vez", "2026-10-14")

    def test_enviar_y_entregar(self):
        pedido = nuevo([CASCO], hoy="2026-10-08")
        pedidos.marcar_enviado(pedido, "Envíos Rápidos", "ER-1", "2026-10-09")
        self.assertEqual(pedido["entrega_prevista"], "2026-10-14")
        pedidos.marcar_entregado(pedido, "2026-10-13")
        self.assertEqual(pedido["estado"], "entregado")

    def test_transferencia_sin_pagar(self):
        pedido = nuevo([CASCO], "transferencia", "2026-10-01")
        self.assertFalse(pedidos.transferencia_caducada(pedido, "2026-10-06"))
        self.assertTrue(pedidos.transferencia_caducada(pedido, "2026-10-07"))
        todos = {"CN-1": pedido}
        self.assertEqual(pedidos.caducar_transferencias(todos, "2026-10-07"), ["CN-1"])
        self.assertEqual(pedido["estado"], "cancelado")

    def test_registrar_pago(self):
        pedido = nuevo([CASCO], "transferencia", "2026-10-01")
        pedidos.registrar_pago(pedido, "2026-10-03")
        self.assertEqual(pedido["estado"], "en preparación")

    def test_plazos(self):
        self.assertTrue(pedidos.admite_pago_plazos(449))
        self.assertFalse(pedidos.admite_pago_plazos(300))

    def test_resumen(self):
        pedido = {"estado": "enviado", "lineas": [CASCO, LUCES], "importe": 99}
        self.assertEqual(pedidos.resumen("CN-1", pedido),
                         "CN-1 · enviado · 1 × Casco Ciudad, 2 × Kit Luces Ciudad · "
                         "99,00 €")


if __name__ == "__main__":
    unittest.main()
