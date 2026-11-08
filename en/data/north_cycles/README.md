# North Cycles · management program

Management program for North Cycles, a bike store in Portland, Oregon: web orders, shipping, returns, warehouse stock, repair shop estimates, invoices, notices to customers and reports. It only uses the Python standard library (3.10 or later).

## Modules

| Module | What it does |
|---|---|
| `config.py` | Business rules: sales tax, rates and time limits (taken from `docs/terms_and_conditions.md`) |
| `database.py` | Reads and saves the JSON files in `data/` |
| `utils.py` | Dates (days, business days, months) and amounts (rounding, dollar format) |
| `shipping.py` | Shipping zone by ZIP code, shipping costs and delivery dates |
| `orders.py` | Creating, canceling, shipping, delivering and paying for orders |
| `returns.py` | Return periods, exceptions, refunds and pickups |
| `stock.py` | Units by size, reservations, restocks and sold-out products |
| `estimates.py` | Tune-ups, warranty and repairs at the repair shop |
| `invoices.py` | Sales tax breakdown and invoice text |
| `customers.py` | Sign-ups, searches and marketing consent |
| `notices.py` | Emails to customers |
| `reports.py` | Sales, average order and counts for management |
| `manage.py` | Console commands, for example `python manage.py sold_out 2026-10-13` |

## Data

`data/` holds a sample database: `catalog.json`, `orders.json`, `stock.json` and `customers.json`. Dates are written as YYYY-MM-DD text and amounts in dollars, sales tax included.

## Tests

From this folder:

```
python -m unittest discover -s tests
```
