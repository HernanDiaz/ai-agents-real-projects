"""Pedidos de la tienda web: importes, alta, cancelación y pagos.

Un pedido es un diccionario con sus líneas (ref, nombre, talla, cantidad y precio),
los gastos de envío, el importe total, el estado y el pago. Los pedidos se guardan
en un diccionario por número (CN-…), como en datos/pedidos.json.
"""
import config
from envios import fecha_entrega_estimada, gastos_envio
from utilidades import dias_entre, formato_euros, redondear


def subtotal(lineas):
    """Suma de las líneas de un pedido: precio por cantidad."""
    return redondear(sum(linea["precio"] * linea["cantidad"] for linea in lineas))


def siguiente_numero(pedidos):
    """El número que toca al próximo pedido: uno más que el mayor (CN-11461…)."""
    mayor = max(int(numero.removeprefix("CN-")) for numero in pedidos)
    return f"CN-{mayor + 1}"


def crear_pedido(cliente_id, lineas, codigo_postal, forma_pago, hoy):
    """Un pedido nuevo, con sus gastos de envío y su estado inicial.

    Con transferencia, el pedido espera al pago; con las demás formas de pago,
    pasa directamente a preparación.
    """
    if not lineas:
        raise ValueError("Un pedido necesita al menos una línea.")
    if forma_pago not in config.FORMAS_PAGO:
        raise ValueError(f"Forma de pago desconocida: {forma_pago}.")
    importe_lineas = subtotal(lineas)
    envio = gastos_envio(importe_lineas, codigo_postal)
    transferencia = forma_pago == "transferencia"
    return {"cliente": cliente_id, "lineas": lineas, "envio": envio,
            "importe": redondear(importe_lineas + envio),
            "estado": "pendiente de pago" if transferencia else "en preparación",
            "fecha_pedido": hoy, "codigo_postal": codigo_postal,
            "pago": {"forma": forma_pago, "recibido": None if transferencia else hoy}}


def se_puede_cancelar(pedido):
    """True mientras el pedido no haya salido del almacén (apartado 2)."""
    return pedido["estado"] in config.ESTADOS_CANCELABLES


def cancelar(pedido, motivo, hoy):
    """Marca el pedido como cancelado. Lanza ValueError si ya salió del almacén."""
    if not se_puede_cancelar(pedido):
        raise ValueError(f"No se puede cancelar un pedido «{pedido['estado']}».")
    pedido["estado"] = "cancelado"
    pedido["motivo"] = motivo
    pedido["fecha_cancelacion"] = hoy
    return pedido


def registrar_pago(pedido, hoy):
    """Anota que ha llegado el pago de un pedido por transferencia."""
    pedido["pago"]["recibido"] = hoy
    if pedido["estado"] == "pendiente de pago":
        pedido["estado"] = "en preparación"
    return pedido


def marcar_enviado(pedido, transportista, seguimiento, hoy):
    """Anota que el pedido ha salido del almacén, con la entrega prevista más tardía."""
    if pedido["estado"] not in ("en preparación", "retrasado"):
        raise ValueError(f"No se puede enviar un pedido «{pedido['estado']}».")
    _, ultima = fecha_entrega_estimada(hoy, pedido["codigo_postal"])
    pedido.update({"estado": "enviado", "transportista": transportista,
                   "seguimiento": seguimiento, "fecha_envio": hoy,
                   "entrega_prevista": ultima})
    return pedido


def marcar_entregado(pedido, hoy):
    """Anota que el transportista ha entregado el pedido."""
    if pedido["estado"] != "enviado":
        raise ValueError(f"No se puede entregar un pedido «{pedido['estado']}».")
    pedido["estado"] = "entregado"
    pedido["fecha_entrega"] = hoy
    return pedido


def marcar_retrasado(pedido, motivo, nueva_fecha):
    """Anota un retraso en la preparación, con su motivo y la nueva fecha prevista."""
    pedido.update({"estado": "retrasado", "motivo": motivo,
                   "entrega_prevista": nueva_fecha})
    return pedido


def transferencia_caducada(pedido, hoy):
    """True si el pedido se paga por transferencia y han pasado más de cinco días
    desde que se hizo sin que haya llegado el pago."""
    if pedido["pago"]["forma"] != "transferencia":
        return False
    return dias_entre(pedido["fecha_pedido"], hoy) > config.DIAS_PAGO_TRANSFERENCIA


def caducar_transferencias(pedidos, hoy):
    """Cancela los pedidos por transferencia cuyo pago no ha llegado a tiempo.
    Devuelve los números de los pedidos cancelados."""
    cancelados = []
    for numero, pedido in pedidos.items():
        if se_puede_cancelar(pedido) and transferencia_caducada(pedido, hoy):
            cancelar(pedido, "transferencia no recibida a tiempo", hoy)
            cancelados.append(numero)
    return cancelados


def admite_pago_plazos(importe):
    """True si el importe permite pagar a plazos (compras de más de 300 euros)."""
    return importe > config.IMPORTE_MINIMO_PLAZOS


def por_estado(pedidos, estado):
    """Los números de los pedidos que están en un estado, ordenados."""
    return sorted(numero for numero, p in pedidos.items() if p["estado"] == estado)


def resumen(numero, pedido):
    """Una línea de texto con lo esencial del pedido, para los listados."""
    productos = ", ".join(f"{linea['cantidad']} × {linea['nombre']}"
                          for linea in pedido["lineas"])
    return (f"{numero} · {pedido['estado']} · {productos} · "
            f"{formato_euros(pedido['importe'])}")
