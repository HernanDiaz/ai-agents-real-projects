# T13 · Low-stock list

We want to know what is about to sell out. Add to stock.py a function `low_stock(stock)`
that returns a list of tuples (ref, size, units) with the sizes that have between 1 and 2
units, sorted by product reference and, within each reference, in the order of the sizes
in the warehouse. The 2 must be in config.py (MIN_STOCK). Sizes at 0 are left out: they
are already in the sold-out report.

— Sean (warehouse)
