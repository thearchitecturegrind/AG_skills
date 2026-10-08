---
description: Drafts a contractor payment application from the schedule of values and progress.
argument-hint: [paste the schedule of values and percent complete or amounts this period]
---
Draft a payment application from $ARGUMENTS.
If $ARGUMENTS is empty, ask for the schedule of values, previous billings, this period's progress, retainage terms, and stored materials.
1. Build the table: line, description, scheduled value, previous, this period, stored, total completed, percent, balance, retainage.
2. Do the arithmetic step by step and show totals; check that no line exceeds its scheduled value.
3. Apply retainage only as the user states the rate; do not assume one.
4. Include approved change orders only if the user lists them with numbers.
5. Flag lines where progress looks out of line with the user's notes.
Mark the output 'DRAFT for review and signature by a licensed professional' at the top. It must not commit the firm to cost, time, or scope; where those are open, say they are reserved.
Output: the draft table, the totals shown step by step, and a list of questions. Certification of payment is for the responsible professional.
