"""Mensajes para los clientes: envío, entrega, cancelación, revisión y promociones."""
import config
from clientes import acepta_publicidad, nombre_corto
from utilidades import formato_euros, formato_fecha, sumar_dias, sumar_meses


def aviso_envio(numero, pedido, cliente):
    """Aviso de que el pedido ha salido del almacén, con su seguimiento."""
    return (f"Hola, {nombre_corto(cliente)}:\n\n"
            f"Tu pedido {numero} ya está en camino con {pedido['transportista']}. "
            f"El número de seguimiento es {pedido['seguimiento']} y la entrega está "
            f"prevista para el {formato_fecha(pedido['entrega_prevista'])}."
            "\n\nUn saludo,\nCiclos Norte")


def aviso_entrega(numero, pedido, cliente):
    """Aviso de pedido entregado, con la fecha límite para devolverlo."""
    entrega = pedido["fecha_entrega"]
    limite = sumar_dias(entrega, config.PLAZO_DEVOLUCION_DIAS)
    return (f"Hola, {nombre_corto(cliente)}:\n\n"
            f"Tu pedido {numero} se entregó el {formato_fecha(entrega)}. Si algo no "
            f"te convence, puedes devolverlo hasta el {formato_fecha(limite)}."
            "\n\nUn saludo,\nCiclos Norte")


def aviso_cancelacion(numero, pedido, cliente):
    """Aviso de pedido cancelado, con el importe que se va a reembolsar."""
    return (f"Hola, {nombre_corto(cliente)}:\n\n"
            f"Hemos cancelado tu pedido {numero} ({pedido['motivo']}). Te devolveremos "
            f"{formato_euros(pedido['importe'])} en un máximo de "
            f"{config.DIAS_REEMBOLSO} días por el mismo medio de pago."
            "\n\nUn saludo,\nCiclos Norte")


def aviso_revision(cliente, fecha_compra):
    """Recordatorio de la primera revisión gratuita de una bicicleta nueva."""
    limite = sumar_meses(fecha_compra, config.MESES_REVISION_GRATIS)
    return (f"Hola, {nombre_corto(cliente)}:\n\n"
            f"La primera revisión de tu bicicleta es gratuita hasta el "
            f"{formato_fecha(limite)}. Después, la revisión básica cuesta "
            f"{formato_euros(config.REVISION_BASICA)}."
            "\n\nUn saludo,\nCiclos Norte")


def destinatarios_promocion(clientes):
    """Los identificadores de los clientes a los que se puede enviar publicidad."""
    return sorted(cliente_id for cliente_id, cliente in clientes.items()
                  if acepta_publicidad(cliente))


def promocion(cliente, texto):
    """Un correo de promoción con el texto de la campaña."""
    return (f"Hola, {nombre_corto(cliente)}:\n\n{texto}\n\n"
            "Si no quieres recibir más correos como este, responde con la palabra "
            "BAJA.\n\nUn saludo,\nCiclos Norte")
