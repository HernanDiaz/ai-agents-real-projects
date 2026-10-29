# Ciclos Norte · programa de gestión

Programa de gestión de la tienda de bicicletas Ciclos Norte (Oviedo): pedidos de la web, envíos, devoluciones, existencias del almacén, presupuestos del taller, facturas, avisos a los clientes e informes. Solo usa la biblioteca estándar de Python (3.10 o posterior).

## Módulos

| Módulo | Qué hace |
|---|---|
| `config.py` | Reglas de negocio: IVA, tarifas y plazos (salen de `docs/condiciones_generales.md`) |
| `base_datos.py` | Lee y guarda los archivos JSON de `datos/` |
| `utilidades.py` | Fechas (días, días laborables, meses) e importes (redondeo, formato en euros) |
| `envios.py` | Zona de envío por código postal, gastos y fechas de entrega |
| `pedidos.py` | Alta, cancelación, envío, entrega y pago de los pedidos |
| `devoluciones.py` | Plazos, excepciones, reembolsos y recogidas |
| `existencias.py` | Unidades por talla, reservas, reposiciones y agotados |
| `presupuestos.py` | Revisiones, garantía y reparaciones del taller |
| `facturas.py` | Desglose del IVA y texto de las facturas |
| `clientes.py` | Altas, búsquedas y consentimiento de publicidad |
| `avisos.py` | Correos para los clientes |
| `informes.py` | Ventas, ticket medio y recuentos para la dirección |
| `gestion.py` | Órdenes de consola, por ejemplo `python gestion.py agotados 2026-10-13` |

## Datos

En `datos/` hay una base de datos de ejemplo: `catalogo.json`, `pedidos.json`, `existencias.json` y `clientes.json`. Las fechas se escriben como texto AAAA-MM-DD y los importes en euros, con el IVA incluido.

## Pruebas

Desde esta carpeta:

```
python -m unittest discover -s tests
```
