# Especificación · Reservar bicicletas agotadas

**Objetivo.** Que un cliente pueda reservar una bicicleta agotada en su talla, sin
prometerle lo que no sabemos.

**Qué hace.** `reserva_agotada(existencias, ref, talla, reposiciones)`, en el módulo
nuevo `reservas.py`, devuelve `{"admite": bool, "fecha": str o None}`:
- admite la reserva si la referencia es de bicicleta (`config.PREFIJOS_BICICLETA`), la
  talla tiene 0 unidades (`unidades` de existencias.py) y hay una reposición prevista
  para esa referencia;
- la fecha es la de la reposición si está confirmada.

**Decisiones que no toma el programa.**
- Sin reposición prevista, no se admite la reserva.
- Con la reposición sin confirmar, se admite, pero la fecha es None: no se promete.
- Los accesorios no se reservan. No se cobra señal.

**Fuera de alcance.** Guardar las reservas; avisar al cliente cuando llegue.

**Criterios de aceptación.**
1. Una bicicleta agotada con reposición confirmada se admite, con su fecha.
2. Si quedan unidades en la talla, no se admite.
3. Sin reposición, no se admite; con reposición sin confirmar, se admite sin fecha.
4. Los accesorios no se admiten.
