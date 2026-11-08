# Specification · A discount for returning customers

**Goal.** Customers who buy often get a discount, without giving away the margin.

**What it does.** `loyalty_discount(orders, customer_id, amount, today)`, in the new
module `loyalty.py`, returns the dollars of discount, rounded to cents:
- 5% of the amount if the customer has 3 or more delivered orders with a
  `delivery_date` in the 365 days before `today` and the amount is over $100;
- at most $25;
- 0 in any other case.

**Decisions the program does not make.** If the customer has any order with a return in
progress, the discount is 0: management decides. Neither the percentage nor the cap
changes by season.

**Out of scope.** Applying the discount to the order; holiday discounts.

**Acceptance criteria.**
1. A customer with many recent delivered orders gets a discount; a new one doesn't.
2. It is 5% on purchases over $100, with a cap of $25.
3. Only orders delivered in the last 365 days count.
4. With a return in progress, the discount is 0.
