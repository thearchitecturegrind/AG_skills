---
description: Writes a letter to the building department.
argument-hint: [who it's to, project, and what you need]
---
Draft a professional letter to the building department based on: $ARGUMENTS
If $ARGUMENTS is empty, ask: what is the purpose (request, clarification, appeal, extension, response), project name or permit number, the specific code section or comment at issue, and what outcome is wanted.
Rules: keep to one page, neutral and courteous, with one clear ask. State facts the user gave; never invent permit numbers, dates, names, or code sections. Use bracketed placeholders for missing items, e.g. [permit number]. Quote any code text only as supplied.
Structure: date and addressee by role; re line; one-paragraph background; the specific request; supporting references by sheet or section; the response date wanted; signature block placeholder.
Output the letter, then a short list of placeholders to fill and facts to verify before sending. Letters carrying legal or safety positions should be reviewed by the licensed professional of record before sending.
If a needed input is missing, do not assume it; list it as a question and give the result as cannot-tell for that part.
Format: a short verdict line first, then a table of Item | Source limit | Your value | Margin | Status, then open questions.
