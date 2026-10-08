---
name: design-parking-layout
description: Lays out parking around stall bays, drive aisles, turning radii, and ramps, checking circulation and fit on the site. Use when testing how many stalls fit, or shaping a lot or garage plan.
---
# Design Parking Layout
Produces a layout approach with dimensioned bays, aisles, and ramps and a count of stalls that fit. A good result shows tradeoffs between stall angle, aisle width, and count.
## Ask first
1. Local stall and aisle dimension standards, pasted or fetched from the zoning code. [fetch and cite]
2. Available area or lot dimensions, entrances, and obstacles such as trees or columns. [required]
3. Design vehicle and any accessible stall requirement text. [passenger car; ask]
## Core rules
- Start with bays and aisles, since two modules fix the efficiency of a lot.
- Use dimensions from the local code or the owner's standard; do not use rule-of-thumb numbers.
- Check turning paths at ends of aisles and at ramps, where layouts commonly break.
- Place accessible stalls and their routes early, before count is final.
- Required count and accessible rules come from the user's text; this tool lays out only.
## Workflow
1. Capture dimensions and constraints.
2. Test one-way and two-way, and at least two stall angles.
3. Add columns, ramp slopes, and entry throat as constraints.
4. Count stalls for each option and compute efficiency as area per stall.
5. Output: Option | Module width | Stalls | Area per stall | Issues | Recommendation.
## If your setup is different
- Structured garage: add column grid, clear heights, and ramp length questions.
- Tight site: consider tandem or valet, and note the zoning text needed to allow them.
- Metric project: convert once and show the conversion.
## Check the result
- [ ] Dimensions are sourced.
- [ ] Circulation was tested at turns and ramps.
- [ ] Counts match the drawn layout.
