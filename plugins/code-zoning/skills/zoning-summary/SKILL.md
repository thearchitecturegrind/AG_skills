---
name: zoning-summary
description: Turns a parcel lookup into an early-design zoning summary: district, permitted use, bulk limits, parking, and review triggers, each cited. Use at the start of a project, feasibility, or when asked 'what can we build here'.
---
# Zoning Summary
Produces a one-to-two page zoning summary tied to the parcel, citing sections and noting unverified items. A good result gives a designer the envelope and the questions to confirm with the zoning office.
## Ask first
1. Parcel address or ID, plus the proposed use. [required]
2. Zoning code text for the district, pasted, or I will fetch the current version from the official source. [fetch]
3. Any overlays, historic districts, or prior approvals known? [ask]
## Core rules
- Use the current official zoning text and map; remembered limits are frequently outdated.
- Record the date of the code and map you read, since amendments are frequent.
- Check overlays and special conditions separately; they can change a district's basic rules.
- Translate each limit to what it means for the building (envelope, program), but keep the quote.
- Zoning interpretation is the zoning official's; flag points to confirm.
## Workflow
1. Resolve the parcel to its district and overlays from the official map.
2. Pull use rules, bulk limits, parking, landscaping, and procedural triggers from the text.
3. Calculate the envelope using lot facts and show the arithmetic.
4. List questions to confirm and approvals possibly needed.
5. Output: Parcel | District and overlays | Table (topic, rule, citation, implication) | Envelope notes | Questions.
## If your setup is different
- Parcel not found: list the data needed.
- Code is online but not current: say so and mark values unverified.
- New York City: switch to the NYC zoning lookup skill.
## Check the result
- [ ] Every rule has a citation.
- [ ] Arithmetic is shown.
- [ ] Unverified items are marked.
