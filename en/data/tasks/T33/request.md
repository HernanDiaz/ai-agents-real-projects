# T33 · Notifying a delayed order

When an order is delayed, the customer finds out because they call us. Make a new
module, delays.py, with a function `delay_notice(number, order, customer,
previous_date)` that tells them about the delay and the new date, with the greeting and
signature of the notices in notices.py (`first_name` is in customers.py, and
`format_date`, in utils.py). The order already comes marked as delayed, with its reason
(`order["reason"]`) and its new expected delivery (`order["expected_delivery"]`).

— Bea (customer service)
