---
name: doc-reader
description: Reads a specification, report, or contract PDF and summarizes it with obligations, deadlines, and unclear terms. Use when someone says summarize this spec, what does this contract require, or explain this report.
---
# Doc Reader
Produces an organized reading of a long text document, pulling out requirements, deadlines, responsibilities, and ambiguities. A good result lets the reader act without reading every page.
## Ask first
1. What do you need from it (summary, obligations, risks, a specific topic)? [obligations and deadlines]
2. Who are you in this document (owner, architect, contractor)? [ask; it changes what matters]
3. Which pages or sections are in scope? [all]
## Core rules
- Cite section and page for every point, because the exact wording governs.
- Report what the document says, not what is typical; practice varies by project.
- Flag defined terms; a capitalized word often has a special meaning set elsewhere.
- Contracts: this is a reading aid, not legal advice; point the user to counsel for decisions.
## Workflow
1. Map the structure: table of contents, parts, appendices, referenced standards.
2. Pull defined terms and key parties.
3. List obligations by party, each with section and any deadline.
4. Collect numbers: dates, amounts, durations, percentages, with the clause they come from.
5. Mark vague or conflicting wording and propose a question for each.
6. Output: one-paragraph summary, obligations table (party, duty, section, deadline), and open questions.
## If your setup is different
- If the PDF is scanned, run text recognition if available or state which pages were unreadable.
- If the document references other documents not supplied, list them as missing.
- If the user wants a legal view, give the facts and suggest a lawyer or the firm's counsel.
## Check the result
- [ ] Every obligation has a section citation.
- [ ] Deadlines and amounts match the source text.
- [ ] Anything I could not read or find is listed as such.
