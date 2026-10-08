---
name: geotech-report-review
description: Reads a geotechnical report and lists the obligations it creates for the design and construction team, such as foundation types, excavation limits, drainage, testing, and special inspections. Use when a soils report arrives and you need to know what it requires.
---
# Geotech Report Review
Produces an obligations table: each recommendation, who must act, in which phase, and where in the report it is. A good result also lists missing or conflicting information.
## Ask first
1. Attach the report, with its date and the boring or test locations plan. [required]
2. What structure is proposed: loads, basement, and site grading? [unknown]
3. Has the design changed since the report? [unknown]
## Core rules
- Separate findings (what was found) from recommendations (what to do); only recommendations create obligations.
- Quote recommendation language with page numbers; wording like 'should' vs 'shall' matters.
- Do not interpret bearing values or structural effects; report them and send to the structural engineer.
- Check the report's own limits, such as depth explored and groundwater timing.
- Structural and safety implications need review by licensed engineers.
## Workflow
1. Read the summary, then the recommendation sections and appendices.
2. Extract each recommendation, with page, and who acts: architect, structural, civil, contractor, or inspector.
3. Note the report's limitations and conflicts with the proposed design.
4. Collect required testing, observation, and inspection items.
5. Output: Recommendation (quote, page) | Owner | Phase | Design impact | Open question.
## If your setup is different
- Report is old or from a neighboring site: flag the limits and suggest asking the geotechnical engineer about suitability.
- No recommendations section: list questions for the engineer instead.
- Contaminated or hazardous finding: route to an environmental professional immediately.
## Check the result
- [ ] Quotes carry page numbers.
- [ ] Owners are named by role.
- [ ] Gaps are listed.
