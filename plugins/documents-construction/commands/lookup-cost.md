---
description: Looks up a cost-per-square-foot benchmark with its source.
argument-hint: [building type, location, year, and quality level]
---
Look up a cost-per-square-foot benchmark for $ARGUMENTS.
If $ARGUMENTS is empty, ask for building type, location, size, quality level, and the year of interest.
1. Search current published sources (cost guides, public agency data, cost-index publications). Open the source and read it; never quote from memory.
2. Report each figure with the source name, publication date, region, and what it includes and excludes.
3. Give a range from at least two sources if you can find them; if only one, say so.
4. Note adjustments needed for location and date; show the arithmetic if you apply an index the source provides.
5. If nothing reliable is found, say 'unverified' and what data the user could provide.
Rules: benchmarks are for early budgeting, not estimates; say so.
Output: table (source, date, region, type, value, notes) and a short caveat.
