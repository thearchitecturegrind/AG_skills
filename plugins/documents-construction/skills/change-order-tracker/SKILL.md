---
name: change-order-tracker
description: Tracks each change from first mention through RFI, directive, pricing, approval, and signed change order. Use when someone says track my changes, which changes are still open, or what is the status of pending changes.
---
# Change Order Tracker
Produces and maintains a change log showing each item's origin, current stage, amount, and time impact. A good result shows nothing falling between a verbal OK and a signed change.
## Ask first
1. Do you have an existing log or should we start one? [start; ask for pasted rows if one exists]
2. What stages does your contract use (RFI, directive, proposal request, change order)? [ask]
3. Who owns the follow-up for each item? [ask]
## Core rules
- Give every item one ID that follows it through each stage, so documents link back.
- Record the date of first mention; late notice can matter under the contract.
- Keep requested, proposed, and approved amounts in separate columns; they differ.
- Never mark an item approved without a signed document reference.
## Workflow
1. Collect source documents: RFIs, emails, meeting minutes, directives, proposals.
2. Create a row per item with ID, description, origin, date first raised, and source reference.
3. Update stage, amounts, time impact, and next action with owner and due date.
4. Flag aging items and those performed without authorization.
5. Compute running totals of pending and approved amounts; show the arithmetic.
6. Output: log table, aging list, and a short status note for the next meeting.
## If your setup is different
- If an item appears in several documents, merge under one ID and list all sources.
- If the contract has notice deadlines, ask for them; do not assume numbers.
- If only email threads exist, extract items and mark the sources as informal.
## Check the result
- [ ] Every row traces to a source document.
- [ ] Totals recompute correctly.
- [ ] Items without signed approval are not shown as approved.
