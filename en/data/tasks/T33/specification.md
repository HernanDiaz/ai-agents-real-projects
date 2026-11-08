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
