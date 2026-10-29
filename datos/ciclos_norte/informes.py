"""Informes para la dirección: ventas, ticket medio y estado de los pedidos.

Se cuentan como ventas los pedidos que no están cancelados. Los importes incluyen
el IVA y los gastos de envío, como en los pedidos.
"""
import base_datos
from utilidades import formato_euros, redondear

ESTADOS_SIN_VENTA = ("cancelado",)


def pedidos_validos(pedidos):
    """Los pedidos que cuentan como venta: todos menos los cancelados."""
    return {numero: p for numero, p in pedidos.items()
            if p["estado"] not in ESTADOS_SIN_VENTA}


def pedidos_del_mes(pedidos, anio, mes):
    """Los pedidos hechos en un mes, por la fecha del pedido."""
    prefijo = f"{anio:04d}-{mes:02d}"
    return {numero: p for numero, p in pedidos.items()
            if p["fecha_pedido"].startswith(prefijo)}


def total_ventas(pedidos):
    """Suma de los importes de los pedidos válidos."""
    return redondear(sum(p["importe"] for p in pedidos_validos(pedidos).values()))


def ticket_medio(pedidos):
    """Importe medio por pedido válido, o 0 si no hay ninguno."""
    validos = pedidos_validos(pedidos)
    if not validos:
        return 0.0
    return redondear(total_ventas(validos) / len(validos))


def ventas_por_categoria(pedidos, catalogo):
    """Importe vendido por categoría del catálogo, sin contar los envíos."""
    categorias = {p["ref"]: p["categoria"] for p in catalogo}
    ventas = {}
    for pedido in pedidos_validos(pedidos).values():
        for linea in pedido["lineas"]:
            categoria = categorias.get(linea["ref"], "sin categoría")
            importe = linea["precio"] * linea["cantidad"]
            ventas[categoria] = redondear(ventas.get(categoria, 0) + importe)
    return dict(sorted(ventas.items(), key=lambda par: par[1], reverse=True))


def recuento_por_estado(pedidos):
    """Cuántos pedidos hay en cada estado."""
    recuento = {}
    for pedido in pedidos.values():
        recuento[pedido["estado"]] = recuento.get(pedido["estado"], 0) + 1
    return recuento


def informe_mensual(anio, mes):
    """Texto con las cifras de un mes, leyendo la base de datos de ejemplo."""
    del_mes = pedidos_del_mes(base_datos.pedidos(), anio, mes)
    filas = [f"Informe de {mes:02d}/{anio}",
             f"Pedidos: {len(del_mes)} ({len(pedidos_validos(del_mes))} válidos)",
             f"Ventas: {formato_euros(total_ventas(del_mes))}",
             f"Ticket medio: {formato_euros(ticket_medio(del_mes))}"]
    for categoria, importe in ventas_por_categoria(del_mes,
                                                   base_datos.catalogo()).items():
        filas.append(f"  {categoria}: {formato_euros(importe)}")
    return "\n".join(filas)
