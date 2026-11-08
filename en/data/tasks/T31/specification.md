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
