"""Reglas de negocio de Ciclos Norte, reunidas en un solo sitio.

Los valores salen de las condiciones generales de venta (docs/condiciones_generales.md).
Los importes están en euros e incluyen el IVA, como los precios de la web.
"""

IVA = 0.21

# --- Envíos (apartado 5) ---
TARIFAS_ENVIO = {"peninsula": 4.95, "baleares": 9.95, "canarias": 14.95}
UMBRAL_ENVIO_GRATIS = 50  # solo en la península, en pedidos de más de 50 euros
PREFIJOS_CP = {"baleares": ("07",), "canarias": ("35", "38")}
DIAS_ENTREGA = {"peninsula": (2, 3), "baleares": (3, 5), "canarias": (5, 7)}

# --- Pedidos y pagos (apartados 2 y 4) ---
FORMAS_PAGO = ("tarjeta", "paypal", "bizum", "transferencia")
ESTADOS_CANCELABLES = ("pendiente de pago", "en preparación")
DIAS_PAGO_TRANSFERENCIA = 5
IMPORTE_MINIMO_PLAZOS = 300  # a plazos, solo en compras de más de 300 euros
PLAZOS_PERMITIDOS = (3, 6, 12)

# --- Devoluciones (apartado 7) ---
PLAZO_DEVOLUCION_DIAS = 30
KM_MAXIMOS_BICICLETA = 10
PREFIJOS_BICICLETA = ("UR", "MT", "CR", "EL", "IN")  # referencias de bicicletas
REFS_HIGIENE = ("RO-2050",)  # culotes: no se admiten desprecintados
DIAS_REEMBOLSO = 14

# --- Almacén ---
MINIMO_EXISTENCIAS = 2  # tallas con 1 o 2 unidades: a punto de agotarse

# --- Taller y garantía (apartados 9 y 10) ---
REVISION_BASICA = 35
MESES_REVISION_GRATIS = 6
TARIFA_HORA_TALLER = 30
MESES_GARANTIA = 24
CAPACIDAD_MINIMA_BATERIA = 0.70  # las baterías deben conservar el 70 % en garantía
PIEZAS_DESGASTE = ("cubierta", "cámara", "pastillas de freno", "cadena", "piñón",
                   "cable")
