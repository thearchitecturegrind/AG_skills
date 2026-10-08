---
name: submittal-log
description: Builds a submittal log from the specification book, listing every required submittal by section with type and review needs. Use when someone says make a submittal log, what submittals are required, or build a submittal register.
---
# Submittal Log
Produces a submittal register with one row per required item, drawn from each spec section's submittal paragraph. A good result is complete before the contractor starts and lets reviewers plan their workload.
## Ask first
1. Do you have the spec book? [ask; without it, only a blank register can be made]
2. What review time and numbering convention apply? [ask]
3. Who reviews each discipline? [ask]
## Core rules
- Take each requirement from the section text, citing section and paragraph.
- Separate action submittals from informational ones, as the spec defines them.
- Include closeout and quality submittals (samples, mockups, test reports), not only shop drawings.
- Do not set durations from memory; use the contract or user input.
## Workflow
1. Read Division 01 submittal procedures and note the definitions and sequencing rules.
2. Go section by section and extract each submittal item.
3. Record: ID, section, paragraph, description, type, reviewer, required before (milestone).
4. Add resubmittal slots if the user wants them.
5. Check for duplicates and sections with no submittal clause.
6. Output: register table plus a summary count by division.
## If your setup is different
- If the spec is scanned, say which pages were read visually.
- If the project is design-build, adapt the reviewer column.
- If the user has a standard template, map to its columns.
## Check the result
- [ ] Every row cites a spec paragraph.
- [ ] Types match the spec's own definitions.
- [ ] No review dates are invented.
