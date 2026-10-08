---
description: Finds a parcel's flood zone and base flood elevation with sources.
argument-hint: [address or parcel ID]
---
Find the flood zone and base flood elevation for: $ARGUMENTS
If $ARGUMENTS is empty, ask for the street address or parcel ID and the city and state.
Use the official flood hazard map service and any local floodplain administrator page. Do not state a zone or elevation from memory. Capture the map panel, effective date, zone, elevation if given, and the vertical datum.
Output a short record: Parcel | Zone | Base flood elevation and datum | Map panel and date | Source URL | Retrieved on.
Add: whether the property is shown partly in the zone, whether a letter of map change may exist, and questions for the local floodplain administrator.
If the sources cannot be reached or the result is ambiguous, say unverified and give the manual steps. This is a research record, not an elevation certificate or a determination.
If a needed input is missing, do not assume it; list it as a question and give the result as cannot-tell for that part.
Format: a short verdict line first, then a table of Item | Source limit | Your value | Margin | Status, then open questions.
