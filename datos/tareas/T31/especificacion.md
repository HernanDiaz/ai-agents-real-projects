# Especificación · Dar de baja a un cliente

**Objetivo.** Que un cliente que lo pide deje de tener sus datos personales en la
tienda, sin romper las facturas que hay que conservar.

**Qué hace.** `baja(clientes, pedidos, cliente_id)`, en el módulo nuevo `bajas.py`:
- cambia el nombre del cliente por «Cliente dado de baja», deja el correo vacío ("") y
  pone `publicidad` a False;
- deja al cliente en el diccionario `clientes`, con su identificador y su ciudad;
- devuelve «hecho».

**Decisiones que no toma el programa.** Si el cliente tiene algún pedido en curso
(estado «pendiente de pago», «en preparación», «enviado», «retrasado» o «devolución en
curso»), la función no cambia nada y devuelve «pendiente»: atención al cliente cierra
antes lo pendiente.

**Fuera de alcance.** Borrar pedidos o facturas; cambiar el formulario de la web.

**Criterios de aceptación.**
1. Tras la baja, el nombre y el correo del cliente ya no están en `clientes`.
2. El cliente sigue en `clientes`, con su ciudad, y sin publicidad.
3. Con un pedido en curso, no cambia nada y devuelve «pendiente»; si no, devuelve «hecho».
