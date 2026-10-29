"""Utilidades de fechas, horas e importes que usan los demás módulos.

Las fechas son textos AAAA-MM-DD y las horas, textos HH:MM, como en los datos.
"""
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal


def fecha(texto):
    """Convierte un texto AAAA-MM-DD en un objeto date."""
    return date.fromisoformat(texto)


def dias_entre(desde, hasta):
    """Días naturales que van de la fecha «desde» a la fecha «hasta»."""
    return (fecha(hasta) - fecha(desde)).days


def sumar_dias(texto, dias):
    """La fecha que cae «dias» días naturales después."""
    return (fecha(texto) + timedelta(days=dias)).isoformat()


def dia_de_la_semana(texto):
    """El día de la semana de una fecha: 0 es lunes y 6, domingo."""
    return fecha(texto).weekday()


def minutos(hora):
    """Una hora HH:MM en minutos desde medianoche."""
    horas, mins = hora.split(":")
    return int(horas) * 60 + int(mins)


def hora(minutos_del_dia):
    """Minutos desde medianoche como hora HH:MM."""
    return f"{minutos_del_dia // 60:02d}:{minutos_del_dia % 60:02d}"


def redondear(importe):
    """Redondea un importe a céntimos, con los medios hacia arriba (2,345 → 2,35)."""
    centimos = Decimal(str(importe)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(centimos)


def formato_euros(importe):
    """Un importe como se escribe en España: 1234.5 → «1.234,50 €»."""
    texto = f"{redondear(importe):,.2f}".replace(",", "X").replace(".", ",")
    return texto.replace("X", ".") + " €"


def formato_fecha(texto):
    """Una fecha AAAA-MM-DD como se escribe en España: 2026-10-15 → 15/10/2026."""
    return fecha(texto).strftime("%d/%m/%Y")
