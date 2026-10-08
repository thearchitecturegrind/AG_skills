---
name: civil-drawing-review
description: Cross-checks the civil engineering set against the architectural set in both directions and lists mismatches in elevations, footprints, utilities, grading, and entrances. Use before a coordination deadline or when sets have been issued separately.
---
# Civil Drawing Review
Produces a mismatch log between civil and architectural sheets, each item citing sheets on both sides. A good result catches conflicts like a door sill below the adjacent grade before the contractor does.
## Ask first
1. Which civil and architectural sheets can I read? List sheet numbers and issue dates. [required]
2. What datum and units does each set use? [check in the notes]
3. Any known open items from the engineer? [none]
## Core rules
- Check both directions; the civil set can contradict the architecture, and the reverse, and each side tends to assume the other is right.
- Compare numbers only after confirming the same datum, units, and issue date; otherwise mismatches are false alarms.
- Cite sheet and detail on both sides for every item so people can resolve it quickly.
- Do not rewrite engineering values or drainage slopes; report discrepancies, and let the engineer decide.
- Anything affecting accessibility or fire access is for a licensed professional to resolve.
## Workflow
1. List the shared elements: building footprint, finished floor elevations, entrances, utilities, loading, fire lanes, retaining walls.
2. Read each on both sets and record the value and sheet.
3. Flag differences, missing items on one side, and conflicting notes.
4. Rank by consequence: life safety and permit blockers first, then cost, then drafting.
5. Output: Item | Civil says (sheet) | Architectural says (sheet) | Conflict | Priority | Owner.
## If your setup is different
- Only one set is available: list what to ask the other consultant for.
- Different datums: record both and require a stated offset before comparing.
- Site work is tiny: reduce to a short list of entrances, elevations, and utility stubs.
## Check the result
- [ ] Both sheet references appear on each line.
- [ ] Datum and units were confirmed.
- [ ] Priorities reflect consequence.
