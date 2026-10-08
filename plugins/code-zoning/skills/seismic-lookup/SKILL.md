---
name: seismic-lookup
description: Records a site's seismic design parameters and the source and date of each, so the structural team gets a traceable input. Use when a project needs seismic design category inputs, site class, or mapped values documented.
---
# Seismic Lookup
Produces a record of the site's seismic parameters with source, date, and edition, plus the questions for the structural engineer. A good result is reproducible by another person.
## Ask first
1. Site address or coordinates. [required]
2. Which reference standard and edition does the adopted code use? [find it]
3. Risk category and site class, if known from the geotechnical report. [unknown]
## Core rules
- Take mapped values from the official hazard tool or table named in the adopted standard, with the retrieval date; values are updated between editions.
- Never state a seismic value from memory.
- Record the exact inputs (coordinates, site class, risk category) used in the tool, since small changes alter results.
- Site class comes from the geotechnical report, not an assumption; if missing, mark it as an open item.
- Structural determinations belong to the engineer of record; this is a documentation aid.
## Workflow
1. Confirm the adopted code edition and the standard it references.
2. Run the official tool or read the official map and capture the output with inputs and date.
3. Record the values, units, and the report or screenshot reference.
4. List open inputs, such as site class and risk category, with owners.
5. Output: Parameter | Value | Source | Date | Inputs used | Open questions.
## If your setup is different
- Tool unavailable: provide manual instructions and mark values unverified.
- Different edition than the tool uses: note the mismatch and ask the engineer.
- Outside the US: use the national hazard maps and standard.
## Check the result
- [ ] Each value has a source and date.
- [ ] Inputs are recorded.
- [ ] Open inputs have owners.
