---
name: design-stair
description: Checks a stair flight against code limits for rise, run, headroom, width, landings, and handrails, showing each number. Use when sizing a stair from floor-to-floor height or reviewing a drawn one.
---
# Design Stair
Produces a stair check with a computed riser count and dimensions, then a table of each element against the sourced limit. A good result catches the headroom and landing errors that appear late.
## Ask first
1. Floor-to-floor height (finished floor to finished floor) and the stair type: egress, accessory, or private. [required]
2. The code limits for the stair type, pasted or fetched and cited. [fetch]
3. Available plan length and width, and what the stair carries in occupants. [required]
## Core rules
- Compute the riser count from total rise first; every other number follows, and rounding errors compound.
- Take limits only from the supplied or sourced text; limits vary with stair type, so confirm the type.
- Check headroom along the entire flight and at landings, not just at the top.
- Show uniformity tolerances as the text gives them.
- Review aid for a licensed professional; stairs are a leading cause of injury and a close reading is worth it.
## Workflow
1. Divide total rise by trial riser height to get a whole number of risers; recompute the exact riser.
2. Select a tread depth and compute the run; check against the plan length.
3. Check width, landing size, handrail height and extensions, guard needs, and headroom.
4. Compare each with the limit and mark the status.
5. Output: Element | Computed or drawn | Limit and source | Status.
## If your setup is different
- Existing stair: record measured values and note which provisions the user says apply to existing stairs.
- Winders, spirals, or alternating tread devices: ask for the text since limits differ.
- Metric: keep a consistent unit and show the conversion.
## Check the result
- [ ] Riser count is a whole number.
- [ ] Headroom was checked along the flight.
- [ ] All limits are cited.
