---
description: Compares massing options by gross floor area, height, and net area
argument-hint: [describe or paste each massing option, with site limits and efficiency target]
---
Compare the massing options in $ARGUMENTS.

If $ARGUMENTS is empty or incomplete, ask for: each option's footprint dimensions or area, number of storeys, floor-to-floor height, and any stated net-to-gross efficiency; the site area; and the limits that apply (height, floor area ratio, coverage, setbacks). Ask the user to paste the governing text for the limits, or offer to look it up from an official source and label what cannot be confirmed as "unverified". Never quote limits from memory.

For each option:
1. Compute gross floor area (footprint times storeys, or the user's figure), showing each multiplication.
2. Compute total height from the floor-to-floor heights given; add roof or parapet only if supplied.
3. Compute net area using the stated efficiency, and say where that figure came from. If none is given, show net as "unknown" and offer a range marked as an assumption.
4. Test each result against each limit and mark it pass, fail, marginal, or cannot-tell, with the numbers and the margin.

Rules: use one unit throughout and show any conversion; state which area definition is used; cite the user value or source for every input; do not invent numbers. Remind the reader once that this is an early feasibility comparison and the planning authority and licensed professional confirm compliance.

Output: an inputs table, a calculation block per option, a comparison table (GFA, height, net area, limit results), a short note on what each option gains and gives up, and the missing information that could change the ranking.
