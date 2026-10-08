---
description: Drafts an architect's supplemental instruction to the contractor with no cost or time change.
argument-hint: [describe the clarification and the sheets or sections affected]
---
Draft an architect's supplemental instruction (ASI) for $ARGUMENTS. An ASI clarifies the documents without changing cost or time.
If $ARGUMENTS is empty, ask what is being clarified, which sheets or sections it touches, and whether any attachments exist.
1. Number placeholder, date, project, to, from, reference to an RFI if any.
2. Description of the clarification, with sheet and section citations.
3. Contractor direction: what to do, written plainly.
4. Add the standard reservation: if the contractor believes this changes cost or time, they must give notice under the contract. Ask the user for the clause; do not cite one from memory.
5. List attachments.
Mark the output 'DRAFT for review and signature by a licensed professional' at the top. It must not commit the firm to cost, time, or scope; where those are open, say they are reserved.
Output: the ASI text and a short list of questions for the reviewer, including whether the item may actually be a change.
