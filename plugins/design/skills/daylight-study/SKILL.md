---
name: daylight-study
description: Estimates daylight depth in each room and finds rooms likely to be dark. Use when someone says "will this room be dark", "check daylight in the plan", "how deep can the room be", or wants an early daylight check before running simulation.
---
# Daylight Study
Makes a quick, transparent estimate of how far useful daylight reaches into each room and lists rooms at risk. A good result states its rule of thumb, its inputs, and that it is a screening step, not a simulation.

## Ask first
1. What are the room depths, window head heights, and orientation (north, south, and so on, and your hemisphere)? [if missing, ask; the estimate depends on all three]
2. Is there anything outside that blocks light (buildings, trees, deep overhangs)? [assume none, and say so]
3. Is there a target you must meet (a rating scheme, local standard, or client goal)? [if so, supply its text; I will not recall thresholds from memory]

## Core rules
- Use a stated rule of thumb for depth (for example a multiple of window head height) only from the user's source or a cited reference, and name it.
- Window head height matters more than width for depth; low heads shorten reach.
- Orientation changes quality, not only quantity: direct sun versus diffuse light.
- Adjacent obstructions and deep reveals reduce the result; flag them as unquantified if no data is given.
- A screening estimate is not compliance; formal results need calculation or simulation by a qualified person.

## Workflow
1. Tabulate each room: depth, width, window head height, window area, orientation, obstruction.
2. Compute the reach from the chosen rule and show the arithmetic.
3. Compare reach with room depth: ok, marginal, or dark; give the margin.
4. Rank dark and marginal rooms by use (a bedroom matters more than a store).
5. Suggest changes: raise the head, add a rooflight, reduce depth, lighten finishes.
6. Output: room table, flagged rooms with numbers, suggested fixes, assumptions, and a note to confirm by simulation.

## If your setup is different
- No dimensions: ask for them, or give a qualitative comment with the label "unquantified".
- Climate with very strong or very weak sky: say the rule of thumb may not transfer and suggest a local method.
- Deep-plan building: recommend simulation early, since rules of thumb fail.

## Check the result
- [ ] The rule used is named and sourced.
- [ ] Each flagged room shows its numbers.
- [ ] The result is labelled as screening.
