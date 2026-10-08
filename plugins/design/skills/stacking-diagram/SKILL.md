---
name: stacking-diagram
description: Checks a programme against floor plate size and core capacity and arranges departments by floor. Use when someone says "make a stacking diagram", "which floor does each department go on", "does the programme fit the floors", or "stack the building".
---
# Stacking Diagram
Allocates departments to floors and tests whether the areas fit each floor plate and its core. A good result shows each floor's available and allocated area, with adjacency and access logic.

## Ask first
1. What are the departments, areas, and headcounts, and which must be near each other or at ground? [ask for the programme and adjacency needs]
2. What are the floor plate gross area, core area, and number of floors? [if unknown, compute a required plate from the programme and show it]
3. Which rules limit floor use (public access, loads, fire separation, height)? [supply the sources; flag unknowns]

## Core rules
- Available area is the floor plate minus core and circulation; use net numbers when comparing with net programme areas.
- Put public and high-traffic functions low, and quiet or secure ones high, then test against the actual adjacencies, not the stereotype.
- Check lift and stair capacity per floor against the population stacked there, using the consultant's method or supplied data.
- Heavy loads (archives, plant, labs) and large-span rooms follow structural limits; flag for the engineer.
- Fire and egress limits by floor are checked by the licensed professional.

## Workflow
1. Compute the available net area per floor and show the sums.
2. Rank departments by constraint: ground access, heavy loads, adjacency, headcount.
3. Place departments floor by floor and total allocated area; show remainder or overrun.
4. Check vertical circulation capacity for the busiest floors.
5. Try one alternative stacking and compare movement between floors.
6. Output: table per floor (department, area, headcount), allocated versus available, adjacencies satisfied or broken, alternative, and a verdict of pass, fail, marginal, or cannot-tell with numbers.

## If your setup is different
- Plate size not fixed: solve for the plate that holds the largest department plus core.
- Podium and tower: stack each part separately and test the connection.
- Campus of low buildings: replace floors with buildings.

## Check the result
- [ ] Each floor shows available, allocated, and remainder.
- [ ] Adjacency breaks are listed.
- [ ] Structural and egress points are flagged.
