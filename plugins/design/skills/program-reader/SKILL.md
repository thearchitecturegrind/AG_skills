---
name: program-reader
description: Examines what a building programme's numbers depend on, such as area basis, headcount, ratios, and assumptions behind each room size. Use when someone says "check this programme", "do these areas make sense", "what are these numbers based on", or inherits a space schedule.
---
# Program Reader
Takes a programme (list of spaces with areas) and exposes the assumptions each number rests on. A good result shows which figures are firm, which are guesses, and which depend on another number.

## Ask first
1. Paste the programme. [if only totals are given, say per-room checks are impossible]
2. What area basis is used (net, gross, rentable)? [if unstated, flag it as the biggest unknown]
3. Where did the numbers come from (client, standard, precedent)? [if unknown, mark each "source not stated"]

## Core rules
- Ask what each number depends on (people, equipment, standard, adjacency); a number with no driver is a placeholder.
- Check arithmetic yourself and show it; totals in inherited schedules are often stale.
- Compare ratios (net to gross, circulation share) to a supplied target or to a cited published benchmark, never from memory.
- Mark dependent numbers: if headcount changes, list which rooms change with it.
- Standards or code-driven sizes must be quoted from the user's source or looked up; otherwise "unverified".

## Workflow
1. Re-add every row and compare with the stated total; show any difference.
2. For each room, write the driver (for example 12 staff times a per-person allowance) or "no driver stated".
3. Identify duplicated, missing, or overlapping rooms.
4. Compute net-to-gross and circulation share from the stated figures.
5. List the five numbers whose change would move the total most.
6. Output: Arithmetic check, Driver table, Sensitivities, Questions for the client.

## If your setup is different
- No area basis given: present results under both net and gross readings.
- Programme in a different unit system: convert once, show the factor, and keep one unit throughout.
- Only a narrative description: build a draft table, labelled as an inference.

## Check the result
- [ ] The total was recomputed and shown.
- [ ] Every room has a driver or the words "not stated".
- [ ] No benchmark is quoted without a source.
