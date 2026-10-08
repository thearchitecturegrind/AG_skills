---
name: design-core
description: Totals the building core (stairs, lifts, shafts, toilets, risers) from your dimensions and gives its share of the floor plate. Use when someone says "size the core", "how much floor area is the core", "core efficiency", or "how big should the core be".
---
# Design Core
Adds up the elements of a core and reports its area and its share of the floor plate. A good result shows each item, the arithmetic, and which sizes came from the user versus a sourced rule.

## Ask first
1. What does the core contain and what are the dimensions of each (stairs, lifts, risers, toilets, plant)? [if a size is missing, ask; I will not guess]
2. What are the floor plate area and number of storeys? [needed for the share]
3. Which rules set stair width, lift count, or toilet counts? [supply your code or the lift supplier's sheets; otherwise I look up official sources and mark unverified items]

## Core rules
- Every size has a source: your drawing, supplier data, or a cited rule; stair, lift, and egress rules differ by place and edition.
- Add wall thickness and clear lobby space, not only equipment footprints, or the core will come out too small.
- Report core area as a share of gross floor plate and also net to gross, and say which basis is used.
- Check the lift count against population with the supplier's or consultant's method, not a rule of thumb from memory.
- Egress stairs, lift lobbies, and fire-fighting provisions are reviewed by the licensed professional; this is a sizing aid only.

## Workflow
1. List each core element with dimensions and source.
2. Compute each footprint including walls; show multiplication.
3. Add circulation and lobby space around the elements.
4. Sum the core and divide by floor plate; show both numbers.
5. Test sensitivity: how does the share change if the lift count or stair width changes.
6. Output: element table, total area, percent of floor plate, assumptions, and items to confirm with the engineer.

## If your setup is different
- Core size unknown for a concept study: give a range from the user's own precedent figures, marked as such.
- Tall building: ask for the lift consultant's sizing, since core share rises with height.
- Residential block: check whether the stair serves as a protected route and ask for the rule.

## Check the result
- [ ] Each dimension has a source.
- [ ] The percentage uses a stated floor plate basis.
- [ ] Safety items are flagged for review.
