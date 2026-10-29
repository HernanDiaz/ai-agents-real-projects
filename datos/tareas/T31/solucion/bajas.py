"""Bajas de clientes que lo piden (apartado 11 de las condiciones generales)."""

EN_CURSO = ("pendiente de pago", "en preparación", "enviado", "retrasado",
            "devolución en curso")


def baja(clientes, pedidos, cliente_id):
    """Da de baja a un cliente que lo pide: borra su nombre y su correo y le quita la
    publicidad, pero lo deja en la lista, porque sus facturas se conservan seis años.
    Si tiene algún pedido en curso no cambia nada: lo decide atención al cliente.
    Devuelve «hecho» o «pendiente»."""
    if any(pedido["cliente"] == cliente_id and pedido["estado"] in EN_CURSO
           for pedido in pedidos.values()):
        return "pendiente"
    clientes[cliente_id].update({"nombre": "Cliente dado de baja", "correo": "",
                                 "publicidad": False})
    return "hecho"
