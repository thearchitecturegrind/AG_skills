---
description: Creates a cover sheet for a document package.
argument-hint: [list what is being sent, to whom, and why]
---
Create a transmittal for $ARGUMENTS.
If $ARGUMENTS is empty, ask: project, date, sender, recipient, method, purpose (for review, for construction, for record), and the list of documents.
1. Header block with project name, number placeholder, date, from, to.
2. Table of items: item number, title, sheet or section, revision or date, copies or format.
3. Purpose of issue and action requested with a response date if the user gave one.
4. Remarks, including what superseded earlier items.
5. Signature line for the sender.
Rules: list only what the user states is included; never assume a document is in the package. Leave unknown revision numbers as placeholders.
Output: a ready-to-use transmittal and a note of any placeholders left.
