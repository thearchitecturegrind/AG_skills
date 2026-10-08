---
name: permit-tracker
description: Maintains one dated record of permits, plan reviews, and inspections for a project. Use when a project has several permits in flight, or when you are asked 'where are we on permits' or 'what inspections are left'.
---
# Permit Tracker
Produces a single permit log with status, dates, reviewer comments received, and inspections, plus the next actions. A good result can be handed to a colleague and read without explanation.
## Ask first
1. Which permits does the project need, and which are already filed? [required]
2. Do you have the permit numbers, dates, and the portal or letters they came from? [paste what you have]
3. Who updates this record, and how often? [project manager, weekly]
## Core rules
- Every row needs a date and a source, since a status without either cannot be trusted.
- Keep one record per permit, with review cycles as sub-rows, because resubmittals are the thing people lose track of.
- Do not guess required inspections; list them from the permit card or authority's list the user supplies, or mark them to be confirmed.
- Record permit numbers only as the user supplies them.
- Flag expirations and lapse rules once, so that no one finds them at closeout.
## Workflow
1. Create a row per permit: type, number, authority, status, filed date, issued date, expiry.
2. Under each, log review cycles with dates and the comment count outstanding.
3. List inspections with status and result, and cross-reference correction items.
4. Add the dependency notes, such as 'foundation permit required before framing inspection'.
5. Output: Permit table, Inspection table, and 'next five actions' with owners by role.
## If your setup is different
- Several jurisdictions: add a column for the authority and keep separate expiry rules.
- Phased project: add a phase column.
- Portal-based tracking exists: treat the portal as source of truth and record its export date.
## Check the result
- [ ] No row lacks a date or source.
- [ ] Review cycles are traceable.
- [ ] Expiries are visible.
