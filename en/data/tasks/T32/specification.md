# Specification · Flagging expensive estimates

**Goal.** The repair shop knows which estimates need the customer's approval before
starting.

**What it does.** `estimate_with_approval(parts, hours, purchase_date, today, cause)`,
in the new module `approvals.py`, returns the estimate from `repair_estimate` with one
more field, `approval`:
- True if the total is over $150 (sales tax included); False if it is $150 or less.
- The threshold is a constant of the module, `APPROVAL_THRESHOLD = 150`.

**Decisions the program does not make.** If any part has the price `None` (not known
yet), `repair_estimate` is not called and no price is made up: it returns
`{"total": None, "approval": True}`. Discounts are not included.

**Out of scope.** The text of the estimate; discounts; changing estimates.py.

**Acceptance criteria.**
1. `approval` is True on an expensive estimate and False on a cheap one.
2. The threshold is $150: $150.01 asks for approval and $150 doesn't.
3. With a part without a price, the total is None and `approval` is True.
