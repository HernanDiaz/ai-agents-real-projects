# Especificación · Avisar de un pedido retrasado

**Objetivo.** Que el cliente sepa por nosotros que su pedido se retrasa, antes de tener
que llamar.

**Qué hace.** `aviso_retraso(numero, pedido, cliente, fecha_anterior)`, en el módulo
nuevo `retrasos.py`, devuelve el texto del aviso, con el saludo («Hola, …:», con
`nombre_corto` de clientes.py) y la firma («Un saludo, Ciclos Norte») de los demás
avisos, el número del pedido, el motivo del retraso (`pedido["motivo"]`), la nueva fecha
prevista (`pedido["entrega_prevista"]`, con `formato_fecha` de utilidades.py) y que, si
quiere cancelarlo, puede contestar a ese correo.

**Decisiones que no toma el programa.**
- Si la nueva fecha es como mucho 2 días posterior a `fecha_anterior`, no se avisa: la
  función devuelve None.
- El aviso no ofrece compensaciones: ni descuentos, ni envío gratis, ni regalos, ni
  reembolsos. Eso lo decide atención al cliente.

**Fuera de alcance.** El aviso de envío; enviar el correo; cambiar avisos.py.

**Criterios de aceptación.**
1. El aviso saluda al cliente, dice el número, el motivo y la nueva fecha, y firma como
   los demás.
2. Con un retraso de 2 días o menos devuelve None.
3. El texto no promete descuentos, envío gratis, regalos ni reembolsos.
