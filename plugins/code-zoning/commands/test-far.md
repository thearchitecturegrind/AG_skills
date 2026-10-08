---
description: Checks floor area ratio, coverage, setback, and height.
argument-hint: [lot data, proposed building data, and the district rules]
---
Check floor area ratio, lot coverage, setbacks, and height against the district rules. Input: $ARGUMENTS
If $ARGUMENTS is empty, ask for: lot area and dimensions, building footprint, floor areas, height, and the district rules (or district name to fetch).
Use only table values or code text the user pastes, or ones you fetch from a current official source and cite with URL and date; never use values from memory. If you cannot verify a value, label it unverified.
Steps:
1. compute floor area ratio: counted floor area divided by lot area, using the code's definition of countable area
2. compute coverage: footprint divided by lot area
3. compare each setback to the minimum, measured to the correct line
4. measure height per the code's measurement method
5. list any exclusions or bonuses used and their source
Show every calculation line by line so the reviewer can follow it.
Result: pass, fail, marginal, or cannot-tell for each of the four tests, with the numbers behind it, the source of each limit, and any missing input.
Zoning definitions vary, so quote the definitions of floor area and height you relied on.
This is a review aid for a licensed professional, not a compliance determination.
