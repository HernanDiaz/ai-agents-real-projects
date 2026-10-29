# Especificación · Descuento para los clientes que repiten

**Objetivo.** Que los clientes que compran a menudo tengan un descuento, sin regalar el
margen.

**Qué hace.** `descuento_fidelidad(pedidos, cliente_id, importe, hoy)`, en el módulo
nuevo `fidelidad.py`, devuelve los euros de descuento, redondeados a céntimos:
- el 5 % del importe si el cliente tiene 3 o más pedidos entregados con `fecha_entrega`
  en los 365 días anteriores a `hoy` y el importe es de más de 100 euros;
- como mucho 25 euros;
- 0 en cualquier otro caso.

**Decisiones que no toma el programa.** Si el cliente tiene algún pedido con una
devolución en curso, el descuento es 0: lo decide dirección. Ni el porcentaje ni el tope
cambian por temporada.

**Fuera de alcance.** Aplicar el descuento al pedido; descuentos de Navidad.

**Criterios de aceptación.**
1. Un cliente con muchos pedidos entregados recientes tiene descuento; uno nuevo, no.
2. Es el 5 % en compras de más de 100 euros, con un tope de 25 euros.
3. Solo cuentan los pedidos entregados en los últimos 365 días.
4. Con una devolución en curso, el descuento es 0.
