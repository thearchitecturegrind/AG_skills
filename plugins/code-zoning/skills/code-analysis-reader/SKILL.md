---
name: code-analysis-reader
description: Reviews someone else's code analysis or code summary and surfaces unstated assumptions, missing inputs, and unsupported conclusions. Use when a consultant, previous designer, or earlier phase handed you a code sheet and you need to know how far to trust it.
---
# Code Analysis Reader
Produces a list of assumptions the analysis relies on but never states, plus claims that lack a source, ranked by how much the design depends on them. A good result tells you what to confirm before building on the analysis.
## Ask first
1. Share the analysis (sheet, memo, or pasted block) and the current project description. [required]
2. Has the design changed since it was written, such as area, use, or stories? [unknown; I will compare dates]
3. Which conclusions does the design lean on most? I will weight those first. [all of them]
## Core rules
- Read for what is absent: a missing occupancy separation or unlisted exception is invisible unless you look for it.
- Distinguish stated facts, derived numbers, and assumptions; only the first can be trusted without work.
- Recompute any derived number from the analysis's own inputs to catch arithmetic or carry-over errors.
- Do not substitute your own code values from memory; list what needs a source check.
- This is a review aid for a licensed professional, not a compliance determination.
## Workflow
1. Inventory each conclusion in the analysis (construction type, area, separation, egress, and so on).
2. For each, note the inputs shown, the code basis cited, and what is not shown.
3. List the implicit assumptions, for example sprinklered, single use, mezzanine counted or not.
4. Compare the analysis inputs with the current drawings and flag mismatches.
5. Output: Conclusion | Basis cited | Unstated assumption | Risk if wrong (high/med/low) | Question to ask.
## If your setup is different
- Analysis cites no edition: add that as the first question and treat every value as unverified.
- Prepared for a different jurisdiction: flag all local-amendment-sensitive conclusions.
- Only a summary was provided with no backup: request the calculations before judging.
## Check the result
- [ ] Each assumption is tied to the conclusion it affects.
- [ ] Mismatches with current drawings are cited by sheet.
- [ ] Nothing is called wrong without a source or recomputation.
