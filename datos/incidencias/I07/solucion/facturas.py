"""Facturas de la clínica: totales, desglose del IVA y texto.

Las facturas son una lista como la de datos/facturas.json:
{"id": "F-0001", "dueno": "D-001", "fecha": "2026-10-16",
 "lineas": [{"concepto": "vacuna polivalente", "importe": 38.0}, …]}.
Los importes incluyen el IVA.
"""
import config
from utilidades import formato_euros, formato_fecha, redondear


def total(lineas):
    """El total de unas líneas, redondeado a céntimos."""
    return redondear(sum(linea["importe"] for linea in lineas))


def desglose_iva(total_con_iva):
    """La base y el IVA de un total que ya lo incluye."""
    base = redondear(total_con_iva / (1 + config.IVA))
    return {"base": base, "iva": redondear(total_con_iva - base)}


def facturas_de(facturas, dueno):
    """Las facturas de un dueño, por fecha."""
    return sorted((f for f in facturas if f["dueno"] == dueno), key=lambda f: f["fecha"])


def texto_factura(factura):
    """La factura como texto, con sus líneas, la base, el IVA y el total."""
    filas = [f"Factura {factura['id']} · {formato_fecha(factura['fecha'])}"]
    for linea in factura["lineas"]:
        filas.append(f"{linea['concepto']:<30}{formato_euros(linea['importe']):>12}")
    suma = total(factura["lineas"])
    partes = desglose_iva(suma)
    filas += [f"{'Base':<30}{formato_euros(partes['base']):>12}",
              f"{'IVA':<30}{formato_euros(partes['iva']):>12}",
              f"{'Total':<30}{formato_euros(suma):>12}"]
    return "\n".join(filas)
