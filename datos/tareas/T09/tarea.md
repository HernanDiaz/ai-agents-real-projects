# T09 · Pago a plazos

Queremos ofrecer el pago a plazos (apartado 4: 3, 6 o 12 meses, más de 300 €). Dos partes:
1. En pedidos.py, `cuotas(importe, meses)`: las cuotas mensuales con dos decimales, iguales
   salvo la última, que ajusta los céntimos para que sumen el importe; si no se admite,
   ValueError.
2. En el texto de la factura, si el pago tiene `plazos`, una línea final «Pago aplazado:
   N cuotas de X», con X la primera cuota.

— Dani (web)
