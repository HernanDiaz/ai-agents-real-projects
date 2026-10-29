"""Facturas de los pedidos.

Los precios de la tienda incluyen el IVA, así que la base imponible se obtiene
dividiendo el total entre 1,21, y la cuota de IVA es lo que falta hasta el total.
"""
import config
from utilidades import formato_euros, formato_fecha, redondear


def desglose_iva(total):
    """Base imponible y cuota de IVA de un importe con el IVA incluido."""
    base = redondear(total / (1 + config.IVA))
    cuota = redondear(total - base)
    return base, cuota


def factura(numero_factura, numero_pedido, pedido, cliente, fecha):
    """Los datos de la factura de un pedido."""
    base, cuota = desglose_iva(pedido["importe"])
    return {"numero": numero_factura, "pedido": numero_pedido, "fecha": fecha,
            "cliente": cliente["nombre"], "lineas": pedido["lineas"],
            "envio": pedido["envio"], "total": pedido["importe"],
            "base": base, "iva": cuota}


def _fila(concepto, importe):
    """Una fila de la factura: el concepto a la izquierda y el importe a la derecha."""
    return f"{concepto:<34}{formato_euros(importe):>14}"


def texto_factura(datos):
    """La factura como texto, lista para imprimir."""
    filas = [f"Factura {datos['numero']} · {formato_fecha(datos['fecha'])}",
             f"Cliente: {datos['cliente']} · Pedido {datos['pedido']}", ""]
    for linea in datos["lineas"]:
        concepto = f"{linea['cantidad']} × {linea['nombre']}"
        filas.append(_fila(concepto, linea["precio"] * linea["cantidad"]))
    filas.append(_fila("Envío", datos["envio"]))
    filas += ["", _fila("Base imponible", datos["base"]),
              _fila(f"IVA ({config.IVA:.0%})", datos["iva"]),
              _fila("Total", datos["total"])]
    return "\n".join(filas)
