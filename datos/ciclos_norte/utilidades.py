"""Utilidades de fechas e importes que usan los demás módulos.

Las fechas viajan como texto en formato AAAA-MM-DD, igual que en los archivos JSON.
"""
import calendar
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal


def fecha(texto):
    """Convierte un texto AAAA-MM-DD en un objeto date."""
    return date.fromisoformat(texto)


def dias_entre(desde, hasta):
    """Días naturales que van de la fecha «desde» a la fecha «hasta»."""
    return (fecha(hasta) - fecha(desde)).days


def sumar_dias(texto, dias):
    """La fecha que cae «dias» días naturales después, como texto AAAA-MM-DD."""
    return (fecha(texto) + timedelta(days=dias)).isoformat()


def sumar_dias_laborables(texto, dias):
    """La fecha que cae «dias» días laborables (de lunes a viernes) después."""
    actual = fecha(texto)
    while dias > 0:
        actual += timedelta(days=1)
        if actual.weekday() < 5:
            dias -= 1
    return actual.isoformat()


def sumar_meses(texto, meses):
    """La misma fecha «meses» meses después. Si ese día no existe en el mes de
    llegada (por ejemplo, el 31 de abril), se usa el último día del mes."""
    inicio = fecha(texto)
    total = inicio.month - 1 + meses
    anio, mes = inicio.year + total // 12, total % 12 + 1
    dia = min(inicio.day, calendar.monthrange(anio, mes)[1])
    return date(anio, mes, dia).isoformat()


def redondear(importe):
    """Redondea un importe a céntimos, con los medios hacia arriba (2,345 → 2,35)."""
    centimos = Decimal(str(importe)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(centimos)


def formato_euros(importe):
    """Un importe como se escribe en España: 1234.5 → «1.234,50 €»."""
    texto = f"{redondear(importe):,.2f}"  # 1,234.50
    texto = texto.replace(",", " ").replace(".", ",").replace(" ", ".")
    return f"{texto} €"


def formato_fecha(texto):
    """Una fecha AAAA-MM-DD como se escribe en España: 2026-10-15 → 15/10/2026."""
    return fecha(texto).strftime("%d/%m/%Y")
