"""Creates tasks T31 to T35 of chapter 9: new functions that someone asks for in plain
words and that involve decisions only the store can make.

Each function goes in a new module, so that the task measures whether the agent
understands what it is asked for, not how well it edits files that already exist.
Besides the usual files (request, contract, data, hidden tests and reference solution),
each task has:
- notes.md: what was said with the people who work at the store, unsorted;
- specification.md: the specification written from those notes;
- criterion_tests/: the tests of the decisions the program must not make on its own
  (thresholds, exceptions, what must not be done). The usual hidden tests check only
  what the request asks for, so that any reasonable interpretation passes them.

Usage: python create_spec_tasks.py; then, python check_bank.py T31 T32 T33 T34 T35
"""
import json
import shutil
from pathlib import Path

FOLDER = Path(__file__).resolve().parent


def create(task_id, title, note, request, signature, notes, specification, contract,
           tests, criterion, solution):
    """Writes the folder of a task, from scratch."""
    folder = FOLDER / task_id
    shutil.rmtree(folder, ignore_errors=True)
    for sub in ("hidden_tests", "criterion_tests", "solution"):
        (folder / sub).mkdir(parents=True, exist_ok=True)
    (folder / "request.md").write_text(
        f"# {task_id} · {title}\n\n{request.strip()}\n\n— {signature}\n",
        encoding="utf-8")
    (folder / "notes.md").write_text(notes.strip() + "\n", encoding="utf-8")
    (folder / "specification.md").write_text(specification.strip() + "\n",
                                             encoding="utf-8")
    (folder / "contract.json").write_text(
        json.dumps({"task": task_id, **contract}, ensure_ascii=False, indent=2)
        + "\n", encoding="utf-8")
    (folder / "meta.json").write_text(
        json.dumps({"id": task_id, "title": title, "type": "feature",
                    "difficulty": 2, "two_sessions": False, "chapter": 9,
                    "note": note}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (folder / "hidden_tests" / f"test_{task_id.lower()}.py").write_text(
        tests.strip() + "\n", encoding="utf-8")
    (folder / "criterion_tests" / f"test_{task_id.lower()}_criterion.py").write_text(
        criterion.strip() + "\n", encoding="utf-8")
    for path, text in solution.items():
        destination = folder / "solution" / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text.strip() + "\n", encoding="utf-8")


def contract(goal, module, criteria, forbidden):
    """The contract of a task: the new module and its tests, nothing else."""
    return {"goal": goal,
            "allowed_paths": [module, f"tests/test_{module}"],
            "forbidden_paths": ["data/", "docs/", *forbidden],
            "acceptance_criteria": criteria}


# --- T31 · Removing a customer -----------------------------------------------
create("T31", "Removing a customer",
       "The request says \"delete\"; the store cannot delete the customer (invoices) "
       "nor remove them while they have orders in progress.",
       """
A customer has written to us asking us to delete her data from the store. Make a new
module, removals.py, with a function `remove_customer(customers, orders, customer_id)`
to remove a customer who asks for it. Customers and orders are dictionaries like the
ones in data/customers.json and data/orders.json: each order has its customer in
"customer" and its "status".
""", "Bea (customer service)",
       """
Notes from a conversation with Bea (customer service) and the accounting firm, on
October 20.

- Bea: "Two or three people a month write asking us to delete them. Right now I do it by
  hand in the customer sheet and I'm always afraid of breaking something."
- The accounting firm: invoices have to be kept for six years, and every invoice shows
  the customer id. If the customer disappears from the list, the old invoices end up
  pointing at nothing. What gets deleted is the personal data: name and email.
- The city on its own is not personal data and we use it in the reports; it can stay.
- Bea: "What I do is put 'Removed customer' as the name and delete the email."
- Once removed, they shouldn't get any marketing, of course.
- Bea, about orders: "If they have an order that hasn't been delivered or a return
  halfway through, I don't touch it: I write to them first to close what's pending.
  That's my call, I don't want the program to do it on its own." Orders in progress are
  the ones awaiting payment, processing, shipped, delayed or with a return in progress.
- In the end, she'd like the function to tell her whether it did it or whether it was
  left pending.
- (Comment from Danny, from the web team: the contact form sometimes sends the email in
  capital letters. Nothing to do with this.)
""",
       """
# Specification · Removing a customer

**Goal.** A customer who asks for it no longer has their personal data at the store,
without breaking the invoices that have to be kept.

**What it does.** `remove_customer(customers, orders, customer_id)`, in the new module
`removals.py`:
- changes the customer's name to "Removed customer", leaves the email empty ("") and
  sets `marketing` to False;
- leaves the customer in the `customers` dictionary, with their id and their city;
- returns "done".

**Decisions the program does not make.** If the customer has any order in progress
(status "awaiting payment", "processing", "shipped", "delayed" or "return in
progress"), the function changes nothing and returns "pending": customer service closes
what is pending first.

**Out of scope.** Deleting orders or invoices; changing the web form.

**Acceptance criteria.**
1. After the removal, the customer's name and email are no longer in `customers`.
2. The customer is still in `customers`, with their city, and without marketing.
3. With an order in progress, nothing changes and it returns "pending"; otherwise, it
   returns "done".
""",
       contract("Remove a customer who asks for it.", "removals.py", [
           "After the removal, the customer's name and email are no longer in "
           "customers.",
           "The customer is still in customers, with their city, and without "
           "marketing.",
           "With an order in progress nothing changes and it returns \"pending\"; "
           "otherwise, \"done\"."],
           ["customers.py", "orders.py", "invoices.py"]),
       '''
"""Task T31: removing a customer (what the request asks for)."""
import json
import unittest

from removals import remove_customer


class T31Tests(unittest.TestCase):

    def test_deletes_name_and_email(self):
        customers = {"CL-0001": {"name": "Laura Green", "email": "laura@example.com",
                                 "city": "Seattle", "marketing": True}}
        orders = {"NC-1": {"customer": "CL-0001", "status": "delivered", "amount": 50}}
        remove_customer(customers, orders, "CL-0001")
        text = json.dumps(customers, ensure_ascii=False)
        self.assertNotIn("Laura", text)
        self.assertNotIn("laura@example.com", text)
''',
       '''
"""Task T31: the store's decisions when removing a customer."""
import unittest

from removals import remove_customer


def sample(status="delivered"):
    customers = {"CL-0001": {"name": "Laura Green", "email": "laura@example.com",
                             "city": "Seattle", "marketing": True}}
    orders = {"NC-1": {"customer": "CL-0001", "status": status, "amount": 50}}
    return customers, orders


class T31CriterionTests(unittest.TestCase):

    def test_does_not_delete_the_customer(self):
        customers, orders = sample()
        self.assertEqual(remove_customer(customers, orders, "CL-0001"), "done")
        self.assertIn("CL-0001", customers)
        self.assertEqual(customers["CL-0001"]["city"], "Seattle")
        self.assertFalse(customers["CL-0001"]["marketing"])

    def test_order_in_progress(self):
        for status in ("awaiting payment", "processing", "shipped", "delayed",
                       "return in progress"):
            customers, orders = sample(status)
            self.assertEqual(remove_customer(customers, orders, "CL-0001"), "pending",
                             status)
            self.assertEqual(customers["CL-0001"]["name"], "Laura Green", status)
''',
       {"removals.py": '''
"""Removing customers who ask for it (section 11 of the terms and conditions)."""

IN_PROGRESS = ("awaiting payment", "processing", "shipped", "delayed",
               "return in progress")


def remove_customer(customers, orders, customer_id):
    """Removes a customer who asks for it: deletes their name and email and turns off
    marketing, but keeps them in the list, because their invoices are kept for six
    years. If they have any order in progress it changes nothing: customer service
    decides. Returns "done" or "pending"."""
    if any(order["customer"] == customer_id and order["status"] in IN_PROGRESS
           for order in orders.values()):
        return "pending"
    customers[customer_id].update({"name": "Removed customer", "email": "",
                                   "marketing": False})
    return "done"
'''})


# --- T32 · Expensive estimates -----------------------------------------------
create("T32", "Flagging expensive estimates",
       "\"Expensive\" has no number in the request; and a part without a price cannot "
       "be estimated on its own.",
       """
At the repair shop we want to know when a repair estimate comes out expensive, so we can
call the customer before starting. Make a new module, approvals.py, with a function
`estimate_with_approval(parts, hours, purchase_date, today, cause)` that makes the
estimate with `repair_estimate` (from estimates.py) and adds an `approval` field to it:
True if we have to call the customer. "parts" is a list of (name, price), as in
`repair_estimate`.
""", "Evan (repair shop)",
       """
Notes from a conversation with Evan (repair shop), on October 21.

- Evan: "When a repair goes over $150, we always call the customer before touching
  anything. Below that, if they left the bike with us to fix it, we fix it."
- The $150 includes sales tax: it's what the customer pays, the total of the estimate.
- Sometimes we write down a part that has to be ordered and we don't know yet how much
  it costs. On the sheet we put it without a price (None). Evan: "Then you can't give a
  total: we call them when we know." He doesn't want the program to make up a price or
  to count it as free.
- With a part without a price, the estimate has no total, and we have to call.
- Evan suggested giving regular customers discounts on big repairs. Martha
  (management) said absolutely not without talking it over first: it's not included.
- (About the text of the estimate: they'd like to put the shop's phone number at the
  bottom. Another day.)
""",
       """
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
""",
       contract("The repair estimate must say whether approval has to be asked for.",
                "approvals.py", [
                    "approval is True on an expensive estimate and False on a cheap "
                    "one.",
                    "The threshold is $150: $150.01 asks for approval and $150 "
                    "doesn't.",
                    "With a part without a price, the total is None and approval is "
                    "True."],
                ["estimates.py", "config.py", "invoices.py"]),
       '''
"""Task T32: flagging expensive estimates (what the request asks for)."""
import unittest

from approvals import estimate_with_approval

OLD = "2020-01-10"   # no warranty
TODAY = "2026-10-13"


class T32Tests(unittest.TestCase):

    def test_expensive(self):
        e = estimate_with_approval([("Fork", 320)], 2, OLD, TODAY, "wear")
        self.assertTrue(e["approval"])
        self.assertEqual(e["total"], 380)

    def test_cheap(self):
        e = estimate_with_approval([("Inner tube", 6)], 0.5, OLD, TODAY, "wear")
        self.assertFalse(e["approval"])
''',
       '''
"""Task T32: the repair shop's decisions about expensive estimates."""
import unittest

from approvals import estimate_with_approval

OLD = "2020-01-10"
TODAY = "2026-10-13"


class T32CriterionTests(unittest.TestCase):

    def test_threshold(self):
        exact = estimate_with_approval([("Wheel", 120)], 1, OLD, TODAY, "wear")
        above = estimate_with_approval([("Wheel", 120.01)], 1, OLD, TODAY, "wear")
        self.assertFalse(exact["approval"])
        self.assertTrue(above["approval"])

    def test_part_without_price(self):
        e = estimate_with_approval([("Chain", 24.9), ("Motor", None)], 2, OLD, TODAY,
                                   "wear")
        self.assertIsNone(e["total"])
        self.assertTrue(e["approval"])
''',
       {"approvals.py": '''
"""Repair shop estimates that need the customer's approval before starting."""
from estimates import repair_estimate

APPROVAL_THRESHOLD = 150   # dollars, sales tax included: above it we call the customer


def estimate_with_approval(parts, hours, purchase_date, today, cause):
    """The estimate of a repair with one more field, "approval": whether to call the
    customer before starting. If any part has no price yet, there is no total and we
    have to call: the repair shop does not make up prices."""
    if any(price is None for _, price in parts):
        return {"total": None, "approval": True}
    estimate = repair_estimate(parts, hours, purchase_date, today, cause)
    return dict(estimate, approval=estimate["total"] > APPROVAL_THRESHOLD)
'''})


# --- T33 · Delay notice ------------------------------------------------------
create("T33", "Notifying a delayed order",
       "The request doesn't say when to notify nor what cannot be promised.",
       """
When an order is delayed, the customer finds out because they call us. Make a new
module, delays.py, with a function `delay_notice(number, order, customer,
previous_date)` that tells them about the delay and the new date, with the greeting and
signature of the notices in notices.py (`first_name` is in customers.py, and
`format_date`, in utils.py). The order already comes marked as delayed, with its reason
(`order["reason"]`) and its new expected delivery (`order["expected_delivery"]`).
""", "Bea (customer service)",
       """
Notes from a conversation with Bea (customer service) and Martha (management), on
October 22.

- Bea: "When an order is delayed, people call us angry. If we tell them first, they call
  less."
- The notice has to say the order number, why it is delayed (the reason the warehouse
  writes down) and the new expected date.
- Bea: "If the delay is a day or two, don't send anything: it arrives almost on time and
  the notice scares people more than it helps." We only notify if the new date is more
  than 2 days after the one it had.
- Martha: "The notice promises nothing: no discounts, no free shipping, no gifts, no
  money back. If a customer asks for compensation, Bea decides case by case."
- If the customer wants to cancel, they can reply to the email; Bea will look at it.
- (Bea also asked for the shipping notice to include the store's phone number. That's
  another task.)
""",
       """
# Specification · Notifying a delayed order

**Goal.** The customer learns from us that their order is delayed, before having to
call.

**What it does.** `delay_notice(number, order, customer, previous_date)`, in the new
module `delays.py`, returns the text of the notice, with the greeting ("Hi …,", with
`first_name` from customers.py) and the signature ("Best regards, North Cycles") of the
other notices, the order number, the reason for the delay (`order["reason"]`), the new
expected date (`order["expected_delivery"]`, with `format_date` from utils.py) and that,
if they want to cancel it, they can reply to that email.

**Decisions the program does not make.**
- If the new date is at most 2 days after `previous_date`, no notice is sent: the
  function returns None.
- The notice offers no compensation: no discounts, no free shipping, no gifts, no
  refunds. Customer service decides that.

**Out of scope.** The shipping notice; sending the email; changing notices.py.

**Acceptance criteria.**
1. The notice greets the customer, says the number, the reason and the new date, and
   signs off like the others.
2. With a delay of 2 days or less it returns None.
3. The text does not promise discounts, free shipping, gifts or refunds.
""",
       contract("Tell the customer that their order is delayed.", "delays.py", [
           "The notice greets, says the number, the reason and the new date, and signs "
           "off.",
           "With a delay of 2 days or less it returns None.",
           "It does not promise discounts, free shipping, gifts or refunds."],
           ["notices.py", "orders.py"]),
       '''
"""Task T33: notifying a delayed order (what the request asks for)."""
import unittest

from delays import delay_notice

CUSTOMER = {"name": "Laura Green", "email": "laura@example.com", "city": "Seattle"}
ORDER = {"customer": "CL-0001", "status": "delayed",
         "reason": "waiting for a part from the supplier",
         "expected_delivery": "2026-10-28"}


class T33Tests(unittest.TestCase):

    def test_notice(self):
        text = delay_notice("NC-10500", ORDER, CUSTOMER, "2026-10-20")
        self.assertIn("Hi Laura", text)
        self.assertIn("NC-10500", text)
        self.assertIn("10/28/2026", text)
        self.assertIn("North Cycles", text)
''',
       '''
"""Task T33: the store's decisions about the delay notice."""
import unittest

from delays import delay_notice

CUSTOMER = {"name": "Laura Green", "email": "laura@example.com", "city": "Seattle"}


def order(date):
    return {"customer": "CL-0001", "status": "delayed",
            "reason": "waiting for a part from the supplier", "expected_delivery": date}


class T33CriterionTests(unittest.TestCase):

    def test_short_delay(self):
        self.assertIsNone(delay_notice("NC-1", order("2026-10-22"), CUSTOMER,
                                       "2026-10-20"))
        self.assertIsNotNone(delay_notice("NC-1", order("2026-10-23"), CUSTOMER,
                                          "2026-10-20"))

    def test_reason_and_no_promises(self):
        text = delay_notice("NC-1", order("2026-10-28"), CUSTOMER, "2026-10-20")
        self.assertIn("waiting for a part from the supplier", text)
        for word in ("discount", "free", "gift", "compensat", "refund"):
            self.assertNotIn(word, text.lower())
''',
       {"delays.py": '''
"""Notices to the customers whose order is delayed."""
from customers import first_name
from utils import days_between, format_date


def delay_notice(number, order, customer, previous_date):
    """Notice that the order is delayed, with the reason and the new date; None if
    the delay is two days or less. It promises no compensation: customer service
    decides that."""
    new = order["expected_delivery"]
    if days_between(previous_date, new) <= 2:
        return None
    return (f"Hi {first_name(customer)},\\n\\n"
            f"Your order {number} is going to be delayed: {order['reason']}. The new "
            f"expected delivery date is {format_date(new)}. If you would rather "
            f"cancel it, just reply to this email."
            "\\n\\nBest regards,\\nNorth Cycles")
'''})


# --- T34 · Backorders --------------------------------------------------------
create("T34", "Backorders for sold-out bikes",
       "The request doesn't say what can be backordered nor whether a date can be "
       "promised.",
       """
On the website, when a bike is sold out in a size, people leave. We want them to be able
to backorder it. Make a new module, backorders.py, with a function
`backorder(stock, ref, size, restocks)` that returns a dictionary with `accepts`
(whether it can be backordered) and `date` (when it will arrive). `restocks` says, by
reference, the date when the supplier's goods arrive and whether it is confirmed:
{"UR-5120": {"date": "2026-11-10", "confirmed": True}}. The stock is like the one in
data/stock.json, and `units(stock, ref, size)`, from stock.py, gives the units of a
size.
""", "Danny (web)",
       """
Notes from a conversation with Danny (web) and Martha (management), on October 23.

- Danny: "If a size is sold out and we don't give them an option, the customer buys
  from another store."
- Only bikes can be backordered (references starting with UR, MT, CR, EL or IN, like
  `BIKE_PREFIXES` in config.py). Accessories can't: they are restocked right away and
  it's not worth it.
- A backorder only makes sense if the size is sold out. If there are units, they should
  buy it.
- Martha: "If the supplier hasn't given us a restock date, no backorder: we can't keep
  people waiting without knowing until when."
- Martha: "And if the date isn't confirmed, don't show it. They can backorder, but
  without promising a date: we'll let them know." Unconfirmed dates nearly always
  change.
- (Danny asked whether we could charge a deposit. Martha: not for now.)
""",
       """
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
""",
       contract("Sold-out bikes must be available for backorder.", "backorders.py", [
           "A sold-out bike with a confirmed restock is accepted, with its date.",
           "If there are units left in the size, it is not accepted.",
           "Without a restock it is not accepted; with an unconfirmed restock, without "
           "a date.",
           "Accessories are not accepted."],
           ["stock.py", "orders.py", "config.py"]),
       '''
"""Task T34: backorders for sold-out bikes (what the request asks for)."""
import unittest

from backorders import backorder

STOCK = {"UR-5120": {"name": "City 3", "units": {"S": 2, "L": 0}}}
RESTOCKS = {"UR-5120": {"date": "2026-11-10", "confirmed": True}}


class T34Tests(unittest.TestCase):

    def test_sold_out(self):
        r = backorder(STOCK, "UR-5120", "L", RESTOCKS)
        self.assertTrue(r["accepts"])
        self.assertEqual(r["date"], "2026-11-10")

    def test_with_units(self):
        self.assertFalse(backorder(STOCK, "UR-5120", "S", RESTOCKS)["accepts"])
''',
       '''
"""Task T34: the store's decisions about backorders."""
import unittest

from backorders import backorder

STOCK = {"UR-5120": {"name": "City 3", "units": {"L": 0}},
         "CA-2010": {"name": "Aero Road Helmet", "units": {"M": 0}}}


class T34CriterionTests(unittest.TestCase):

    def test_no_restock(self):
        self.assertFalse(backorder(STOCK, "UR-5120", "L", {})["accepts"])

    def test_unconfirmed(self):
        r = backorder(STOCK, "UR-5120", "L",
                      {"UR-5120": {"date": "2026-11-10", "confirmed": False}})
        self.assertTrue(r["accepts"])
        self.assertIsNone(r["date"])

    def test_accessory(self):
        r = backorder(STOCK, "CA-2010", "M",
                      {"CA-2010": {"date": "2026-11-10", "confirmed": True}})
        self.assertFalse(r["accepts"])
''',
       {"backorders.py": '''
"""Backorders for bikes that are sold out in a size."""
import config
from stock import units


def backorder(stock, ref, size, restocks):
    """Whether a bike that is sold out in a size can be backordered, and for when.
    Only bikes, with no units and with an expected restock; if the restock is not
    confirmed it is accepted without a date, so as not to promise what we don't know."""
    restock = restocks.get(ref)
    accepts = (ref.startswith(config.BIKE_PREFIXES)
               and units(stock, ref, size) == 0 and restock is not None)
    date = restock["date"] if accepts and restock["confirmed"] else None
    return {"accepts": accepts, "date": date}
'''})


# --- T35 · Loyalty discount --------------------------------------------------
create("T35", "A discount for returning customers",
       "The request doesn't say how much, for whom or with what cap: those are "
       "management's decisions.",
       """
We want to reward customers who come back with a discount. Make a new module,
loyalty.py, with a function `loyalty_discount(orders, customer_id, amount, today)` that
returns the dollars of discount on a new purchase of that amount. Orders are a
dictionary like the one in data/orders.json, by order number: each order has its
customer in "customer", its "status" and, if it has been delivered, its
"delivery_date" (YYYY-MM-DD).
""", "Martha (management)",
       """
Notes from a meeting with Martha (management) and Bea (customer service), on
October 24.

- Martha: "I want the people who buy from us often to notice it, but without giving
  away the margin."
- Returning customer: one who has 3 or more delivered orders in the last 365 days (by
  delivery date). Canceled orders and the ones not yet delivered don't count.
- The discount is 5% of the amount, and only on purchases over $100. With a cap: at most
  $25 per purchase.
- Bea: "If the customer has a return in progress, better not: sometimes they're
  customers with an open problem." Martha: "No automatic discount there; if needed, I'll
  decide."
- It's rounded to cents.
- (Martha mentioned that over the holidays it might go up to 10%. She'll decide in
  December; for now, 5%.)
""",
       """
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
""",
       contract("A discount for returning customers.", "loyalty.py", [
           "A customer with many recent delivered orders gets a discount; a new one "
           "doesn't.",
           "It is 5% on purchases over $100, with a cap of $25.",
           "Only orders delivered in the last 365 days count.",
           "With a return in progress, the discount is 0."],
           ["orders.py", "invoices.py", "customers.py"]),
       '''
"""Task T35: a discount for returning customers (what the request asks for)."""
import unittest

from loyalty import loyalty_discount

TODAY = "2026-10-24"


def delivered(customer, date):
    return {"customer": customer, "status": "delivered", "amount": 80,
            "order_date": date, "delivery_date": date}


ORDERS = {f"NC-{n}": delivered("CL-0001", f"2026-0{n}-10") for n in range(1, 9)}


class T35Tests(unittest.TestCase):

    def test_returning(self):
        self.assertGreater(loyalty_discount(ORDERS, "CL-0001", 400, TODAY), 0)

    def test_new(self):
        self.assertEqual(loyalty_discount(ORDERS, "CL-0099", 400, TODAY), 0)
''',
       '''
"""Task T35: management's decisions about the loyalty discount."""
import unittest

from loyalty import loyalty_discount

TODAY = "2026-10-24"


def order(status, date):
    return {"customer": "CL-0001", "status": status, "amount": 80,
            "order_date": date, "delivery_date": date}


THREE = {f"NC-{n}": order("delivered", f"2026-0{n}-10") for n in (3, 5, 7)}


class T35CriterionTests(unittest.TestCase):

    def test_percentage_and_cap(self):
        self.assertEqual(loyalty_discount(THREE, "CL-0001", 200, TODAY), 10)
        self.assertEqual(loyalty_discount(THREE, "CL-0001", 1000, TODAY), 25)
        self.assertEqual(loyalty_discount(THREE, "CL-0001", 100, TODAY), 0)

    def test_only_the_last_year(self):
        old = {f"NC-{n}": order("delivered", f"2024-0{n}-10") for n in (3, 5, 7)}
        self.assertEqual(loyalty_discount(old, "CL-0001", 200, TODAY), 0)
        two = {k: v for k, v in THREE.items() if k != "NC-7"}
        self.assertEqual(loyalty_discount(two, "CL-0001", 200, TODAY), 0)

    def test_return_in_progress(self):
        with_return = dict(THREE, **{"NC-9": order("return in progress", "2026-09-20")})
        self.assertEqual(loyalty_discount(with_return, "CL-0001", 200, TODAY), 0)
''',
       {"loyalty.py": '''
"""Discount for returning customers."""
from utils import days_between, round_cents


def loyalty_discount(orders, customer_id, amount, today):
    """The dollars of discount on a purchase for a returning customer: 5% on
    purchases over $100, with a cap of $25, if they have 3 or more delivered orders in
    the last year. No discount if they have a return in progress: management
    decides."""
    theirs = [o for o in orders.values() if o["customer"] == customer_id]
    if any(o["status"] == "return in progress" for o in theirs):
        return 0
    recent = [o for o in theirs if o["status"] == "delivered"
              and 0 <= days_between(o["delivery_date"], today) <= 365]
    if len(recent) < 3 or amount <= 100:
        return 0
    return round_cents(min(amount * 0.05, 25))
'''})
