---
description: Checks a building's allowable area.
argument-hint: [construction type, use, stories, sprinklers, and area]
---
Check whether a building's area is within the allowable area for its construction type and use. Input: $ARGUMENTS
If $ARGUMENTS is empty, ask for: use group, construction type, number of stories, sprinkler status, frontage conditions, and actual area per floor, plus the allowable area table.
Use only table values or code text the user pastes, or ones you fetch from a current official source and cite with URL and date; never use values from memory. If you cannot verify a value, label it unverified.
Steps:
1. read the base tabular area for the use and type
2. apply each increase or reduction the text allows, one per line, with its condition
3. compute the allowable area per floor and total
4. compare to actual area and state the margin
5. note mixed-use rules if more than one use is present
Show every calculation line by line so the reviewer can follow it.
Result: pass, fail, marginal, or cannot-tell, with the numbers behind it, the source of each limit, and any missing input.
Increases depend on conditions you must confirm with the user, such as open frontage; list each as confirmed or assumed.
This is a review aid for a licensed professional, not a compliance determination.
