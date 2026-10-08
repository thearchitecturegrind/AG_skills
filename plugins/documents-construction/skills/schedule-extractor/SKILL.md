---
name: schedule-extractor
description: Extracts door, window, and finish schedules from a drawing PDF into CSV files. Use when someone says pull the schedule out of this PDF, convert the door schedule to Excel, or make a CSV of the finish schedule.
---
# Schedule Extractor
Produces one CSV per schedule with a log of what was extracted and what could not be read. A good result matches the PDF row for row.
## Ask first
1. Which PDF and which pages hold schedules? [ask or scan for them]
2. What columns do you need? [all that appear]
3. Can code execution and a PDF library be used? [check; else do manually]
## Core rules
- Preserve cell values exactly; do not correct apparent errors, and list them instead.
- Row count in the CSV must equal the PDF; compare it.
- Mark uncertain reads from scans instead of guessing.
- Keep original headers and add a source page column.
## Workflow
1. Locate schedule sheets by title text or by looking at page images.
2. Try text and table extraction; if the output is scrambled, use page images and read visually.
3. Build one CSV per schedule with headers and a page column.
4. Compare row counts and a few random cells against the page.
5. Record anomalies: blanks, merged cells, duplicate marks.
6. Output: file paths, a preview of the first rows, and an exceptions log.
## If your setup is different
- If no PDF tools are available, give the extracted table in chat and say it is not saved as CSV.
- If the PDF is scanned, note that text recognition may introduce errors.
- If schedules span multiple pages, join them and note page breaks.
## Check the result
- [ ] Row counts match the source.
- [ ] Uncertain cells are flagged.
- [ ] CSV opens with correct headers.
