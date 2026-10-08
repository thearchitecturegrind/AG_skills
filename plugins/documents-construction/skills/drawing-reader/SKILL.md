---
name: drawing-reader
description: Reads an architectural drawing PDF and explains what each sheet shows, what is missing, and what to ask. Use when someone says read this drawing, what am I looking at, walk me through this set, or uploads plans they cannot interpret.
---
# Drawing Reader
Produces a sheet-by-sheet reading of a drawing PDF in plain language, with open questions. A good result lets a non-designer understand what is proposed and what is unclear.
## Ask first
1. Which sheets or pages matter most? [all sheets, in order]
2. What is your role (owner, contractor, student, staff)? [non-designer reader]
3. Is this a PDF with selectable text or a scan? If you cannot open the file, ask the user to re-upload or paste the sheet index.
## Core rules
- Cite sheet number and page for every statement, so the reader can find it again.
- Say what a sheet shows before what it means; interpretation without evidence misleads.
- Separate what is drawn from what is assumed; drawings often omit what the spec covers.
- Define symbols and abbreviations in a few words on first use (for example, 'typ.' means typical).
## Workflow
1. Read the title block and sheet index; note project phase, date, revision, and scale.
2. Find the legend, abbreviations, and general notes before reading plans.
3. Go sheet by sheet: state what it shows, key dimensions or tags, and notes that govern.
4. Trace references (callout bubbles, section marks) to the sheet they point to; flag broken ones.
5. List items that look unfinished, conflicting, or missing, each with a sheet reference.
6. Output: a short summary, a sheet-by-sheet table (sheet, shows, notes), then a numbered question list.
## If your setup is different
- If the PDF is scanned or low resolution, say which values you could not read rather than guessing.
- If the set uses a non-standard sheet numbering system, build your own index and state it.
- If the drawings are from another country, ask which standards and units apply before interpreting symbols.
## Check the result
- [ ] Every claim has a sheet or page reference.
- [ ] Unreadable items are marked 'could not read', not filled in.
- [ ] This is a reading aid; design decisions and code compliance remain with the licensed architect.
