---
name: adjacency-matrix
description: Builds a room adjacency matrix from observed movement and use rather than stated closeness. Use when someone says "build an adjacency matrix", "which rooms need to be next to each other", "bubble diagram inputs", or has observation, interview, or log data about how people move.
---
# Adjacency Matrix
Produces a matrix of how strongly pairs of spaces relate, based on counted or described movement, not on what people say they want. A good result ranks pairs by evidence and flags where stated wishes and observed behaviour disagree.

## Ask first
1. What movement data exists (counts, observation notes, interviews, badge logs, walk-throughs)? [if none, build a stated-closeness matrix and label it "stated, not observed"]
2. Which rooms or functions are in scope? [ask for the list]
3. Who moves (staff, patients, visitors, goods)? [separate them if there is more than one group]

## Core rules
- Weight observed trips over stated preference, since people tend to overstate the importance of what they like and understate routine trips.
- Record frequency and also how time-critical each trip is; a rare emergency link can outrank a daily convenience.
- Keep user groups separate when their routes should not cross.
- Include negative adjacencies (noise, privacy, cleanliness) as well as positive ones.
- Use a small scale (for example essential, desirable, neutral, avoid) and define it in the output.

## Workflow
1. List spaces and user groups.
2. Tally trips per pair per group from the supplied data; show counts.
3. Convert counts to the scale using stated thresholds (agree them with the user).
4. Add qualitative needs: privacy, noise, hygiene, supervision.
5. Compare with stated wishes and list disagreements.
6. Output: Matrix (table with scale key), Evidence column citing the source for each strong link, Conflicts between observed and stated, Suggested grouping.

## If your setup is different
- Only interviews: mark every cell "stated" and suggest a short observation to confirm the top ten links.
- New building with no users yet: use data from the closest comparable operation the user supplies.
- Many rooms: group into zones first, then detail within zones.

## Check the result
- [ ] Every strong link cites a count or note.
- [ ] Observed versus stated is distinguished.
- [ ] Negative adjacencies are included.
