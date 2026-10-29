"""Reglas de la Clínica Veterinaria Naranco, reunidas en un solo sitio.

Los precios están en euros e incluyen el IVA, como los de la lista de precios
(docs/tarifas.md).
"""

IVA = 0.21

# --- Citas ---
APERTURA = "09:00"           # primera cita del día
CIERRE = "14:00"             # la última cita empieza media hora antes
DURACION_CITA = 30           # minutos
DIAS_DE_CONSULTA = (0, 1, 2, 3, 4)   # de lunes (0) a viernes (4)

# --- Vacunas ---
DIAS_AVISO_VACUNA = 30       # se avisa de las vacunas que vencen en los próximos 30 días

# --- Precios ---
TARIFAS = {
    "consulta": 35.0,
    "urgencia": 60.0,
    "revisión anual": 30.0,
    "vacuna rabia": 30.0,
    "vacuna polivalente": 38.0,
    "vacuna leishmaniosis": 45.0,
    "vacuna trivalente felina": 36.0,
    "vacuna leucemia felina": 40.0,
    "desparasitación": 15.0,
    "limpieza dental": 120.0,
    "cura": 22.0,
    "análisis de sangre": 65.0,
}
