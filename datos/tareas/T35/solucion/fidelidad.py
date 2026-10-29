"""Descuento para los clientes que repiten."""
from utilidades import dias_entre, redondear


def descuento_fidelidad(pedidos, cliente_id, importe, hoy):
    """Los euros de descuento de una compra para un cliente que repite: el 5 % en
    compras de más de 100 euros, con un tope de 25, si tiene 3 pedidos entregados o más
    en el último año. Sin descuento si tiene una devolución en curso: lo decide
    dirección."""
    suyos = [p for p in pedidos.values() if p["cliente"] == cliente_id]
    if any(p["estado"] == "devolución en curso" for p in suyos):
        return 0
    recientes = [p for p in suyos if p["estado"] == "entregado"
                 and 0 <= dias_entre(p["fecha_entrega"], hoy) <= 365]
    if len(recientes) < 3 or importe <= 100:
        return 0
    return redondear(min(importe * 0.05, 25))
