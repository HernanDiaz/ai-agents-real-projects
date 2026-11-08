# T32 · Flagging expensive estimates

At the repair shop we want to know when a repair estimate comes out expensive, so we can
call the customer before starting. Make a new module, approvals.py, with a function
`estimate_with_approval(parts, hours, purchase_date, today, cause)` that makes the
estimate with `repair_estimate` (from estimates.py) and adds an `approval` field to it:
True if we have to call the customer. "parts" is a list of (name, price), as in
`repair_estimate`.

— Evan (repair shop)
