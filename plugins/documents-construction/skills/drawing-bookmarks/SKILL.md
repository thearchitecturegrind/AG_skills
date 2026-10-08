---
name: drawing-bookmarks
description: Adds bookmarks to a flat drawing-set PDF and builds an index of sheet numbers and titles. Use when someone says bookmark my drawing set, make the PDF navigable, or create a sheet index for this PDF.
---
# Drawing Bookmarks
Produces a bookmarked PDF and a sheet index from a set with no navigation. A good result lets any reader jump to a sheet by number and title.
## Ask first
1. Where is the PDF and how many pages? [ask]
2. What bookmark style do you want (by discipline, flat list)? [by discipline]
3. Should the original stay untouched? [yes; save a new copy]
## Core rules
- Never overwrite the original; work on a copy, in case extraction is wrong.
- Read sheet numbers from title blocks, not from page order; pages may be out of order.
- Check every bookmark target; a mislabelled bookmark is worse than none.
- Report sheets you could not read instead of guessing.
## Workflow
1. Check whether code execution and a PDF library are available; if not, go to the alternative below.
2. Extract text from the title block area on each page; fall back to page images for scans.
3. Build the index: page, sheet number, title, discipline.
4. Create bookmarks grouped by discipline (or flat) and write the new PDF.
5. Open the result and spot-check at least five bookmarks.
6. Output: the new PDF path, the index table, and a list of unreadable pages.
## If your setup is different
- If no PDF library is available, deliver the index table and the exact steps to add bookmarks in a PDF editor.
- If sheets are scanned, say text recognition is needed first and offer to run it if available.
- If numbering is unusual, ask for the firm's convention.
## Check the result
- [ ] Original file is unchanged.
- [ ] Spot-checked bookmarks land on the right page.
- [ ] Unreadable pages are listed.
