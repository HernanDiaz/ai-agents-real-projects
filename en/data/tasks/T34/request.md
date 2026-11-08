# T34 · Backorders for sold-out bikes

On the website, when a bike is sold out in a size, people leave. We want them to be able
to backorder it. Make a new module, backorders.py, with a function
`backorder(stock, ref, size, restocks)` that returns a dictionary with `accepts`
(whether it can be backordered) and `date` (when it will arrive). `restocks` says, by
reference, the date when the supplier's goods arrive and whether it is confirmed:
{"UR-5120": {"date": "2026-11-10", "confirmed": True}}. The stock is like the one in
data/stock.json, and `units(stock, ref, size)`, from stock.py, gives the units of a
size.

— Danny (web)
