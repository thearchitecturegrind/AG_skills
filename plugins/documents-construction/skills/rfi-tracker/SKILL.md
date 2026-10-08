---
name: rfi-tracker
description: Maintains the request-for-information log and surfaces patterns across questions and answers. Use when someone says RFI log, track RFIs, which RFIs are overdue, or what are the RFIs telling us.
---
# RFI Tracker
Produces a running RFI log with status and ageing, plus an analysis of repeated causes. A good result shows which drawing or spec problems generate the most questions.
## Ask first
1. Do you have the RFIs or an existing log? [ask]
2. What response time does the contract allow? [ask; do not assume]
3. Who is the reviewer for each discipline? [ask]
## Core rules
- Log date sent, date due, and date answered, because the gaps are the story.
- Record whether the answer changed scope, cost, or time; that is what matters later.
- Tag each RFI with sheet or spec section and cause, so patterns appear.
- Keep the question and the answer wording unedited.
## Workflow
1. Enter each RFI: number, date, question summary, sheet or section, from, to.
2. Record due date from the contract period the user gives.
3. Update status, response date, and whether it triggered a change.
4. Flag overdue and aging items.
5. Count by cause (missing info, conflict, clarification, substitution) and by sheet or trade.
6. Output: log table, overdue list, and a short pattern note with suggested fixes.
## If your setup is different
- If RFIs come as emails, extract fields and cite the email date.
- If numbering is inconsistent, assign a tracking ID and map to the original.
- If you lack the response period, show elapsed days only.
## Check the result
- [ ] Every row has dates and a location reference.
- [ ] Patterns cite the RFIs behind them.
- [ ] Cost or time impacts are flagged for the change process.
