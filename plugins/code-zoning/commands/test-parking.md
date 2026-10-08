---
description: Checks required parking count and accessible spaces.
argument-hint: [use, size, and the parking rules]
---
Check required parking count and accessible spaces against what is provided. Input: $ARGUMENTS
If $ARGUMENTS is empty, ask for: use and size basis (area, units, or seats), the parking ratio table, reductions or maximums that apply, the accessible space table, and the count provided.
Use only table values or code text the user pastes, or ones you fetch from a current official source and cite with URL and date; never use values from memory. If you cannot verify a value, label it unverified.
Steps:
1. find the ratio row for each use
2. compute required spaces per use and sum, showing rounding
3. apply any reductions (transit, shared parking) only if the text and the user's facts support them
4. compute the accessible spaces from the sourced table, including any van or access aisle conditions
5. compare with provided spaces
Show every calculation line by line so the reviewer can follow it.
Result: required, provided, and pass, fail, marginal, or cannot-tell, with the numbers behind it, the source of each limit, and any missing input.
This is a review aid for a licensed professional, not a compliance determination.
