---
name: schedule-builder
description: Builds a door, window, finish, or room schedule from drawings or notes in a table ready for the drawing set. Use when someone says make a door schedule, build a finish schedule, or create a room schedule.
---
# Schedule Builder
Produces a clean schedule table with consistent marks and every item traced to the plans. A good result has no duplicate marks and no blank required fields.
## Ask first
1. Which schedule (door, window, finish, room)? [ask]
2. Where is the source data (plans, model export, notes)? [ask]
3. Does your firm have a column template or naming convention? [ask; else use plain headings]
## Core rules
- Marks must be unique and match the tags on the plans.
- Do not invent sizes, ratings, or hardware; leave a clear placeholder if the source is silent.
- Fire ratings and accessibility values come from the plans or code the user supplies; flag for professional review.
- Keep one row per item, with a source sheet.
## Workflow
1. Confirm schedule type and columns.
2. Extract each item from the plans or data with its mark and location.
3. Fill dimensions, types, materials, and finishes from the source.
4. Mark missing fields TBD and list them.
5. Check for duplicate marks, untagged items, and mismatches with room names.
6. Output: table, CSV-ready if requested, and an exceptions list.
## If your setup is different
- If the data comes from a model export, map its columns and state the mapping.
- If drawings are scans, read carefully and tag low-confidence entries.
- If units differ, ask which to display.
## Check the result
- [ ] Marks are unique.
- [ ] Every row cites a source.
- [ ] TBD items are listed.
