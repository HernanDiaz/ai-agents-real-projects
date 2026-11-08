# T09 · Paying in installments

We want to offer payment in installments (section 4: 3, 6 or 12 months, over $300). Two parts:
1. In orders.py, `installments(amount, months)`: the monthly installments with two decimals,
   all equal except the last one, which adjusts the cents so that they add up to the
   amount; if installments are not allowed, ValueError.
2. In the invoice text, if the payment has `installments`, a final line "Installment plan:
   N payments of X", where X is the first installment.

— Danny (web)
