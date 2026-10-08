---
name: space-program
description: Tracks the room list, target areas, and designed areas of a project and shows the differences as the design develops. Use when someone says "set up the space programme", "track areas against the brief", "update the room schedule", or "are we over on area".
---
# Space Program
Maintains a table of rooms with target and designed areas, variances, and totals. A good result is a living schedule where every change is traceable and the totals are always recomputed.

## Ask first
1. What are the rooms, counts, and target areas, and where do the targets come from? [if no source, mark "source not stated"]
2. How are designed areas measured (net or gross, from drawings or a model)? [ask; mixing bases hides errors]
3. What is the allowed tolerance and the overall area cap? [if none, ask the client's expectation]

## Core rules
- Recompute totals each time; do not trust carried-over sums.
- Keep target and designed values in separate columns with the date and source of each.
- Show variance in area and in percent, and highlight items beyond tolerance.
- Keep unplanned spaces visible (circulation, plant, storage) rather than folding them into a factor.
- Record who approved each change to target areas, since scope creep starts there.

## Workflow
1. Build the table: room, count, unit target, total target, designed area, variance, source, notes.
2. Add subtotals by department or zone.
3. Add circulation and plant lines from the user's stated ratios, or leave placeholders.
4. Compute net, gross, and ratio between them; show the arithmetic.
5. List out-of-tolerance rooms and the likely cause.
6. Output: the table, totals, variances, change log, and open questions.

## If your setup is different
- Spreadsheet supplied: keep its structure, add missing columns, and report formula errors found.
- Room data in a model: ask which schedule or export they use, and whether it matches the drawn rooms.
- Early stage: use ranges for targets (min and max) instead of single values.

## Check the result
- [ ] Totals match the rows when added by hand.
- [ ] Each target has a source or says "not stated".
- [ ] Variances beyond tolerance are flagged.
