# T12 · Invoice numbering and credit notes

The accounting firm asks us to number invoices consecutively by year. Two parts:
1. In invoices.py, `next_invoice_number(issued, date, series="I")`: given the numbers
   already issued (such as "I2026-0007") and the date, the next one for that year and
   series ("I2026-0008"); the first one of each year is 0001.
2. `credit_note(original, amount, number, date)` for returns (series C): a `corrects`
   field with the number of the original invoice, and total, before tax and tax as
   negative amounts.

— Nora (accounting)
