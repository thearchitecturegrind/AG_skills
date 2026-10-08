---
name: design-egress
description: Verifies the exit count, exit width, exit separation, and travel distance for a floor plan, showing each calculation. Use when laying out stairs and exits, or when checking an egress plan against the adopted code.
---
# Design Egress
Produces an egress verification table covering four tests with inputs, arithmetic, and sources. A good result flags the test that governs and the margin left.
## Ask first
1. Occupancy classification, sprinkler status, floor area, and occupant load (or I can compute it from your table). [required]
2. Code text or tables for the four tests, pasted, or I will fetch the adopted ones and cite them. [fetch]
3. Plan sheet showing exits, doors, and the longest paths. [required for distances]
## Core rules
- Run all four tests: count, width, separation, and travel; a plan can pass three and fail the fourth.
- Measure travel along the actual path, not straight lines, because code measures walking distance.
- Pull factors and limits from supplied or officially sourced text only.
- Show the margin, since 'passes by one foot' is a design risk worth knowing.
- This is a review aid for a licensed professional, not a life-safety determination.
## Workflow
1. Establish occupant load per space and per floor, with inputs.
2. Determine the required number of exits and verify the plan has them.
3. Calculate required width from occupant load and the sourced factor; compare with provided clear widths.
4. Check separation between exits and the longest travel and dead-end distances.
5. Output: Test | Required (with source) | Provided (sheet) | Margin | Status (pass/fail/marginal/cannot-tell).
## If your setup is different
- Plan is undimensioned: mark travel as cannot-tell and list the missing lengths.
- Existing building: ask which chapter or path governs and use its tables.
- Different jurisdiction: swap the source tables and keep the four tests.
## Check the result
- [ ] All four tests appear.
- [ ] Margins are shown.
- [ ] Every limit is sourced.
