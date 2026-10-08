---
name: design-occupancy-load
description: Computes occupant load by use group and by space from a supplied or officially sourced factor table, with the arithmetic shown. Use when sizing exits, plumbing, or when asked 'what is the occupant load'.
---
# Design Occupancy Load
Produces an occupant load schedule: each space, area basis, load factor, and resulting count, rolled up by floor and building. A good result is auditable line by line.
## Ask first
1. Paste the occupant load factor table for your adopted code, or I will fetch and cite it. [fetch]
2. A room list with areas and uses; say whether areas are gross or net, since the factor basis differs. [required]
3. Any fixed seating counts, which override area-based figures? [none]
## Core rules
- Match the area basis (gross or net) to the table's own definition; mismatches silently skew the load.
- Use the factor from the supplied table only, never from memory.
- Round as the code instructs, and show that rounding.
- Count spaces with multiple uses by the rule in the text, flagging the ambiguity for the user.
- Result informs life-safety design and needs verification by a licensed professional.
## Workflow
1. Gather the table, area basis definitions, and the room list.
2. Assign each space its use row and factor.
3. Compute area divided by factor, show it, and round per the text.
4. Add fixed seating or other special counts.
5. Output: Space | Use row | Area | Factor | Load | Total by floor | Building total | Source.
## If your setup is different
- Areas are unknown: give a formula template and ask for the numbers.
- Mixed uses within a room: show both options and let the user pick with a reason.
- Another code: use that code's table with the same arithmetic.
## Check the result
- [ ] Every load shows its area and factor.
- [ ] Gross vs net was confirmed.
- [ ] Totals reconcile.
