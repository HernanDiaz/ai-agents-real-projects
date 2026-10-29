"""Avisos a los clientes cuyo pedido se retrasa."""
from clientes import nombre_corto
from utilidades import dias_entre, formato_fecha


def aviso_retraso(numero, pedido, cliente, fecha_anterior):
    """Aviso de que el pedido se retrasa, con el motivo y la nueva fecha; None si el
    retraso es de dos días o menos. No promete compensaciones: las decide atención al
    cliente."""
    nueva = pedido["entrega_prevista"]
    if dias_entre(fecha_anterior, nueva) <= 2:
        return None
    return (f"Hola, {nombre_corto(cliente)}:\n\n"
            f"Tu pedido {numero} se va a retrasar: {pedido['motivo']}. La nueva fecha "
            f"de entrega prevista es el {formato_fecha(nueva)}. Si prefieres "
            f"cancelarlo, contesta a este correo."
            "\n\nUn saludo,\nCiclos Norte")
