# T35 · A discount for returning customers

We want to reward customers who come back with a discount. Make a new module,
loyalty.py, with a function `loyalty_discount(orders, customer_id, amount, today)` that
returns the dollars of discount on a new purchase of that amount. Orders are a
dictionary like the one in data/orders.json, by order number: each order has its
customer in "customer", its "status" and, if it has been delivered, its
"delivery_date" (YYYY-MM-DD).

— Martha (management)
