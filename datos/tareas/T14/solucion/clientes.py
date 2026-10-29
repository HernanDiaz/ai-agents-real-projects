"""Clientes de la tienda web.

Los clientes son un diccionario por identificador (CL-…), como en
datos/clientes.json. El campo «publicidad» indica si el cliente ha autorizado
recibir información comercial (apartado 11 de las condiciones generales).
"""
import re

PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def correo_valido(correo):
    """True si el texto tiene forma de dirección de correo."""
    return bool(PATRON_CORREO.match(correo))


def nombre_corto(cliente):
    """El nombre de pila del cliente, para los saludos."""
    return cliente["nombre"].split()[0]


def normalizar_correo(correo):
    """El correo sin espacios en los extremos y en minúsculas, para compararlo."""
    return correo.strip().lower()


def buscar_por_correo(clientes, correo):
    """El identificador del cliente con ese correo, o None si no hay ninguno.
    No distingue mayúsculas ni tiene en cuenta los espacios de los extremos."""
    buscado = normalizar_correo(correo)
    for cliente_id, cliente in clientes.items():
        if normalizar_correo(cliente["correo"]) == buscado:
            return cliente_id
    return None


def pedidos_de_cliente(pedidos, cliente_id):
    """Los números de los pedidos de un cliente, del más reciente al más antiguo."""
    suyos = [(pedido["fecha_pedido"], numero) for numero, pedido in pedidos.items()
             if pedido["cliente"] == cliente_id]
    return [numero for _, numero in sorted(suyos, reverse=True)]


def alta(clientes, nombre, correo, ciudad, publicidad=False):
    """Da de alta un cliente nuevo y devuelve su identificador.

    Lanza ValueError si el correo no es válido o ya está registrado.
    """
    if not correo_valido(correo):
        raise ValueError(f"Correo no válido: {correo}.")
    if buscar_por_correo(clientes, correo):
        raise ValueError(f"Ya hay un cliente con el correo {correo}.")
    mayor = max((int(c.removeprefix("CL-")) for c in clientes), default=0)
    cliente_id = f"CL-{mayor + 1:04d}"
    clientes[cliente_id] = {"nombre": nombre, "correo": correo, "ciudad": ciudad,
                            "publicidad": publicidad}
    return cliente_id


def acepta_publicidad(cliente):
    """True si el cliente ha autorizado recibir información comercial."""
    return cliente.get("publicidad", True)
