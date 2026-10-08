---
name: document-diff
description: Compares two versions of a document (spec, contract, report, scope letter) and finds every change, especially ones not called out in the cover note. Use when someone says what changed, find unflagged changes, or compare these two versions.
---
# Document Diff
Produces a change list between two document versions, split into flagged and unflagged changes. A good result catches quiet edits to numbers, dates, scope, or responsibility.
## Ask first
1. Which file is older and which is newer? [ask; never guess from filenames]
2. Is there a cover note or revision list saying what changed? [ask for it to compare against]
3. What matters most (money, dates, scope, wording)? [all]
## Core rules
- Compare text line by line, not by memory; small word swaps change meaning.
- Treat changes to numbers, dates, 'shall'/'may', and 'by others' as high priority.
- Mark a change 'flagged' only if the cover note or redline mentions it.
- Report moved text separately from changed text so it is not mistaken for deletion.
## Workflow
1. Confirm both versions and their dates; note page counts.
2. If a script or diff tool is available, run it on extracted text; otherwise compare section by section.
3. Record each change: location, old wording, new wording.
4. Rate impact: cost, schedule, scope, responsibility, or editorial.
5. Check each against the cover note and mark flagged or unflagged.
6. Output: a table (location, old, new, impact, flagged?) with unflagged high-impact items first.
## If your setup is different
- If one version is a scan, extract text first and say that errors may come from recognition.
- If only a redline is supplied, verify it against the clean copy; redlines can miss changes.
- If versions differ in layout, compare by section number, not page.
## Check the result
- [ ] Every change shows old and new wording with a location.
- [ ] Unflagged changes are clearly separated.
- [ ] Anything I could not compare is listed.
