---
name: climate-zone-mapper
description: Records a site's climate zone and the envelope requirements tied to it, with the source for each. Use when starting energy compliance, filling in a code sheet, or checking which insulation or glazing table applies.
---
# Climate Zone Mapper
Produces a short record of the site's climate zone, the energy code and edition in force, and the envelope requirement rows that apply, each cited. A good result can be pasted into the cover sheet and defended.
## Ask first
1. Project address or county, so the zone can be found from an official map or table. [required]
2. Which energy code and edition does the jurisdiction enforce? [I will look it up]
3. Building type and whether it is residential or commercial for the code's purposes. [required]
## Core rules
- Take the zone from the energy code's county or location table or an official government map; climate maps copied from other websites are often outdated.
- Record moisture and humidity classifications as well as the number, because they change requirements.
- Never state insulation or glazing values from memory; extract them from the table the user supplies or one fetched and cited.
- Mark the date and edition, as zones and tables change between editions.
- Local amendments can override the base table; ask for them.
## Workflow
1. Resolve the location to the zone using an official source and record the URL.
2. Confirm the adopted energy code edition and any amendments.
3. Identify the correct building category and the table or compliance path used.
4. Extract envelope requirement rows (roof, wall, floor, slab, fenestration) only from supplied or verified text.
5. Output: Site | Zone and moisture class | Code and edition | Requirement table with source | Open questions.
## If your setup is different
- Site is on a zone boundary or in a split county: flag it and ask the authority which applies.
- Performance path planned: record the zone and note that the table is only the baseline.
- Non-US project: use the local climate classification and its official source.
## Check the result
- [ ] Zone has a source URL and date.
- [ ] Table values match the text supplied or cited.
- [ ] Amendments are asked about.
