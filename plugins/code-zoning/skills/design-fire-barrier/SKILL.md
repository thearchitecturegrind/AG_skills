---
name: design-fire-barrier
description: Traces a fire-rated wall, floor, or shaft through a plan and sections to find where the rating stops, such as at penetrations, joints, corners, and the roof. Use when drawing rated assemblies or checking continuity.
---
# Design Fire Barrier
Produces a continuity trace of a rated assembly, listing each place the rating could break and the detail or listing needed. A good result tells you which junctions lack a detail.
## Ask first
1. Which assembly is rated, what rating is required, and where did the requirement come from (citation)? [required]
2. Plan and section sheets where the assembly appears. [required]
3. Do you have listed assembly or product data for the wall or floor? [none]
## Core rules
- Rating is only as good as its weakest point, so walk the whole boundary instead of checking the wall midpoint.
- Do not state a rating, hourly value, or listing number from memory; use the user's source or a cited official listing.
- Check each junction type: top of wall, floor, curtain wall edge, corner, penetration, duct, door, and expansion joint.
- Record the detail that resolves each junction or mark it as missing.
- Review aid for a licensed professional; a testing or listing authority decides.
## Workflow
1. Mark the barrier on the plan from end to end, noting closed loops or terminations.
2. At each break point, note the condition and what the drawings show.
3. Check wall-to-deck and wall-to-floor continuity on the sections.
4. List penetrations and openings and the protection each needs.
5. Output: Location | Condition | Detail shown | Gap | Fix needed | Sheet.
## If your setup is different
- Shaft or stair enclosure: trace vertically and note the top and bottom conditions.
- Existing building: add a field verification column since concealed conditions govern.
- Different rating system: use its vocabulary, but keep the trace.
## Check the result
- [ ] Barrier is traced end to end.
- [ ] Each gap has a named fix.
- [ ] No rating value is unsourced.
