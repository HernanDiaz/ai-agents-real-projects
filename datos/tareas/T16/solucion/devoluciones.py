"""Devoluciones de pedidos (apartado 7 de las condiciones generales).

Empezó como el pequeño programa de devoluciones del agente del libro anterior. Ahora
trabaja con las líneas de cada pedido, la zona de envío y las excepciones: bicicletas
con kilómetros y culotes desprecintados.
"""
import config
from envios import zona
from existencias import reponer
from utilidades import formato_euros, redondear, sumar_dias


def fecha_limite_devolucion(pedido):
    """Último día para devolver un pedido: 30 días después de la entrega o, si se
    entregó en la campaña de Navidad, el 31 de enero siguiente si es más tarde."""
    entrega = pedido["fecha_entrega"]
    limite = sumar_dias(entrega, config.PLAZO_DEVOLUCION_DIAS)
    inicio, fin = config.CAMPANA_NAVIDAD
    if inicio <= entrega[5:] <= fin:
        limite_navidad = f"{int(entrega[:4]) + 1}-{config.LIMITE_NAVIDAD}"
        limite = max(limite, limite_navidad)
    return limite


def se_puede_devolver(pedido, hoy):
    """True si el pedido está entregado y no ha pasado su fecha límite."""
    if pedido["estado"] != "entregado":
        return False
    return hoy <= fecha_limite_devolucion(pedido)


def es_bicicleta(ref):
    """True si la referencia es de una bicicleta (urbana, montaña, carretera…)."""
    return ref.startswith(("UR", "MT", "CR", "EL", "IN"))


def motivo_rechazo(pedido, linea, hoy, km=0, desprecintado=False):
    """Por qué no se puede devolver una línea del pedido, o None si se puede."""
    if not se_puede_devolver(pedido, hoy):
        return "El pedido no está entregado o ha terminado el plazo de devolución."
    if es_bicicleta(linea["ref"]) and km > 10:
        return "La bicicleta tiene más de 10 km recorridos."
    if linea["ref"] in config.REFS_HIGIENE and desprecintado:
        return "Por higiene, no se admiten culotes desprecintados."
    return None


def importe_reembolso(pedido, devueltas):
    """Importe que se reembolsa por las unidades devueltas.

    «devueltas» es una lista de {"ref": …, "cantidad": …}. Los gastos del envío
    original solo se reembolsan si se devuelve el pedido completo.
    """
    precios = {linea["ref"]: linea["precio"] for linea in pedido["lineas"]}
    importe = sum(precios[d["ref"]] * d["cantidad"] for d in devueltas)
    if len(devueltas) == len(pedido["lineas"]):
        importe += pedido["envio"]
    return redondear(importe)


def coste_recogida(pedido):
    """Lo que paga el cliente por la recogida: nada en la península; desde las
    islas, la tarifa de envío de su zona."""
    zona_pedido = zona(pedido["codigo_postal"])
    if zona_pedido == "peninsula":
        return 0.0
    return config.TARIFAS_ENVIO[zona_pedido]


def fecha_limite_reembolso(fecha_recepcion):
    """Último día para reembolsar: 14 días desde que llega el producto devuelto."""
    return sumar_dias(fecha_recepcion, config.DIAS_REEMBOLSO)


def registrar_devolucion(pedido, devueltas, hoy, existencias):
    """Anota una devolución aceptada: el pedido pasa a «devolución en curso», se
    guarda el importe que hay que reembolsar y las unidades vuelven al almacén."""
    if not se_puede_devolver(pedido, hoy):
        raise ValueError("El pedido no se puede devolver.")
    tallas = {linea["ref"]: linea["talla"] for linea in pedido["lineas"]}
    for devuelta in devueltas:
        reponer(existencias, devuelta["ref"], tallas[devuelta["ref"]],
                devuelta["cantidad"])
    pedido["estado"] = "devolución en curso"
    pedido["devolucion"] = {"fecha": hoy, "lineas": devueltas,
                            "importe": importe_reembolso(pedido, devueltas)}
    return pedido


def resumen_devolucion(numero, pedido, devueltas, hoy):
    """Texto para el cliente con el resultado de su solicitud de devolución."""
    if not se_puede_devolver(pedido, hoy):
        return f"El pedido {numero} no se puede devolver."
    importe = formato_euros(importe_reembolso(pedido, devueltas))
    texto = f"Devolución del pedido {numero} aceptada: se reembolsarán {importe}."
    recogida = coste_recogida(pedido)
    if recogida:
        texto += f" La recogida desde las islas cuesta {formato_euros(recogida)}."
    return texto
