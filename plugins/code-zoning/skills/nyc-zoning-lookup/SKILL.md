---
name: nyc-zoning-lookup
description: Answers New York City zoning questions with citations to official city sources, and says plainly what could not be verified. Use for NYC lots only, when you need district, regulations, or overlays for a specific property.
---
# NYC Zoning Lookup
Produces an answer about a New York City lot with each fact tied to an official city source and date, and a separate list of what remains unverified. A good result lets you rely on the cited facts and chase the rest.
## Ask first
1. The NYC address or borough, block, and lot. [required]
2. The question: district, permitted use, floor area, yard, height, parking, or overlay? [required]
3. Is this for existing conditions or a proposed change? [unknown]
## Core rules
- Applies to New York City only; for other places, say so and stop rather than applying NYC rules.
- Use official city sources, such as the city's zoning map and resolution text, the property data portal, and department of buildings records; do not use memory or third-party summaries.
- State what could not be verified, because zoning text and maps are amended and a stale answer can sink a design.
- Cite the source, section, and retrieval date with each fact.
- Zoning interpretation is a professional judgment; this is a research aid.
## Workflow
1. Confirm the lot identifiers and resolve the zoning district and any overlays from the official map.
2. Locate the relevant sections of the zoning resolution for the question and quote them.
3. Apply the lot facts and show any arithmetic.
4. Record amendments or pending text changes found and mark gaps.
5. Output: Answer | Facts table (fact, source, date) | Unverified items | Next step (e.g., ask the city for confirmation).
## If your setup is different
- Lot not found or sources unreachable: say so and provide the manual steps to reach the official tools.
- Special district or landmark status: flag it and note that separate rules may apply.
- Not in New York City: decline and offer a general zoning summary instead.
## Check the result
- [ ] Every fact has an official source and date.
- [ ] Unverified items are listed.
- [ ] No values came from memory.
