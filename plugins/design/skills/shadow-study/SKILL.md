---
name: shadow-study
description: Calculates sun angles and shadow reach for a massing, date, and location using real solar geometry. Use when someone says "shadow study", "how far will it shade the neighbour", "sun angles on December 21", or "overshadowing check".
---
# Shadow Study
Computes sun position and the shadow cast by a simple massing for chosen dates and hours, and reports the numbers. A good result shows the geometry, the assumptions, and what it cannot capture.

## Ask first
1. Where is the site (latitude and longitude, or city) and what is true north versus plan north? [if only a city, look up coordinates and cite the source]
2. What are the massing dimensions and heights, and the dates and hours to test? [defaults: the two solstices and an equinox, hourly in local solar daytime]
3. Which neighbours or spaces are sensitive, and is there a rule to meet? [supply the planning text; I will not quote thresholds from memory]

## Core rules
- Compute sun altitude and azimuth with a recognised algorithm (for example NOAA or a maintained library) in code if available, and state the method; do not rely on remembered tables.
- State the time convention (local clock, daylight saving, or solar time), because an hour of error moves shadows.
- Shadow length on flat ground equals height divided by tan(altitude); show it for each time and add the direction opposite the sun's azimuth.
- Treat terrain, trees, and neighbouring buildings as excluded unless the user supplies them; say so.
- Planning compliance is for the responsible planner; this is an analytical aid.

## Workflow
1. Record inputs and assumptions, including date, time zone, and orientation.
2. Compute altitude and azimuth for each time and show a table.
3. Compute shadow length and direction for the top edge of the massing; show a worked example.
4. Project shadow tips to the plan and describe or tabulate which areas are covered and for how long.
5. Compare with any rule supplied.
6. Output: assumptions, sun table, shadow results, hours of shade at key points, limitations, and the code used.

## If your setup is different
- No code environment: do one worked hand example and give the formula, and mark the rest as an estimate.
- Southern hemisphere: the formulas hold; check seasons and the sun's north-side path.
- Sloping ground: ask for levels and adjust height for each point.

## Check the result
- [ ] The method and time convention are stated.
- [ ] A worked example can be followed.
- [ ] Exclusions (trees, neighbours, slope) are listed.
