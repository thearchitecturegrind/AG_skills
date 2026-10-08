---
description: Writes a general note and identifies the correct sheet for it.
argument-hint: [describe the requirement the note should state]
---
Write a drawing general note for $ARGUMENTS.
If $ARGUMENTS is empty, ask what the note must say, which discipline, and whether the firm has a general notes sheet.
1. Draft the note in short imperative sentences, one requirement per note.
2. Recommend where it belongs: the general notes sheet for the discipline, or a plan sheet if it applies only to one area. Explain why in a sentence.
3. Check whether it duplicates or conflicts with the spec or existing notes if the user supplies them; avoid restating spec text that could drift.
4. Suggest a note number placeholder in the firm's pattern.
Rules: do not cite code sections or standards from memory; if one is needed, ask the user for it or label it unverified. A licensed professional must approve the wording.
Output: the note, the sheet recommendation, and any conflicts found.
