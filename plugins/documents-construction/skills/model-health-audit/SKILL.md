---
name: model-health-audit
description: Audits a BIM model for issues that slow it down, reduce accuracy, or complicate sharing. Use when someone says model health check, why is Revit slow, audit my model, or clean up before sharing.
---
# Model Health Audit
Produces a prioritized audit of a building information model, with counts and fixes. A good result lets the BIM lead act on the worst items first.
## Ask first
1. Which software and version? [ask]
2. Can you export a warnings list, file size, and view counts, or give live access? [ask; otherwise use supplied screenshots]
3. Is the model worked on by a team, linked, or going to a consultant? [ask]
## Core rules
- Report the numbers you actually see; do not assume typical thresholds, and label any rule of thumb as such.
- Fix order matters: errors and duplicates first, then bloat, then naming.
- Test changes on a copy; cleaning can delete used content.
- Do not modify the model without the user's go-ahead.
## Workflow
1. Collect metrics: file size, warnings count, links, imported CAD, views and sheets, in-place families.
2. Look for duplicate or overlapping elements, unplaced rooms, unused views and families.
3. Check worksets or shared setup, units, coordinates, and link health.
4. Check naming and standards against the user's convention.
5. If a live connection is available, query the model; otherwise ask for exports.
6. Output: findings table (area, count, risk, fix, effort) and a ranked action list.
## If your setup is different
- For other software, map the checks to its equivalents and say so.
- If the model is huge, sample and state the sampling.
- If no data can be obtained, give a manual checklist instead of findings.
## Check the result
- [ ] Findings have counts from the supplied data.
- [ ] Fixes are separated into safe and risky.
- [ ] No changes were made without confirmation.
