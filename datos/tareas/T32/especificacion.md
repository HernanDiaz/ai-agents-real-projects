# Especificación · Avisar de los presupuestos caros

**Objetivo.** Que el taller sepa qué presupuestos necesitan la aprobación del cliente
antes de empezar.

**Qué hace.** `presupuesto_con_aprobacion(piezas, horas, fecha_compra, hoy, causa)`, en
el módulo nuevo `aprobaciones.py`, devuelve el presupuesto de `presupuesto_reparacion`
con un campo más, `aprobacion`:
- True si el total supera 150 euros (IVA incluido); False si es de 150 o menos.
- El umbral es una constante del módulo, `UMBRAL_APROBACION = 150`.

**Decisiones que no toma el programa.** Si alguna pieza tiene precio `None` (todavía no
se sabe), no se llama a `presupuesto_reparacion` ni se inventa un precio: devuelve
`{"total": None, "aprobacion": True}`. Los descuentos no entran.

**Fuera de alcance.** El texto del presupuesto; descuentos; cambiar presupuestos.py.

**Criterios de aceptación.**
1. `aprobacion` es True en un presupuesto caro y False en uno barato.
2. El umbral es 150 euros: 150,01 pide aprobación y 150 no.
3. Con una pieza sin precio, el total es None y `aprobacion` es True.
