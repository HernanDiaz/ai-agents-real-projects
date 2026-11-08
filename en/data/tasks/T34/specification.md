# Specification · Backorders for sold-out bikes

**Goal.** A customer can backorder a bike that is sold out in their size, without us
promising what we don't know.

**What it does.** `backorder(stock, ref, size, restocks)`, in the new module
`backorders.py`, returns `{"accepts": bool, "date": str or None}`:
- it accepts the backorder if the reference is a bike (`config.BIKE_PREFIXES`), the
  size has 0 units (`units` from stock.py) and there is an expected restock for that
  reference;
- the date is the restock date if it is confirmed.

**Decisions the program does not make.**
- Without an expected restock, the backorder is not accepted.
- With an unconfirmed restock, it is accepted, but the date is None: nothing is
  promised.
- Accessories cannot be backordered. No deposit is charged.

**Out of scope.** Storing the backorders; notifying the customer when it arrives.

**Acceptance criteria.**
1. A sold-out bike with a confirmed restock is accepted, with its date.
2. If there are units left in the size, it is not accepted.
3. Without a restock, it is not accepted; with an unconfirmed restock, it is accepted
   without a date.
4. Accessories are not accepted.
