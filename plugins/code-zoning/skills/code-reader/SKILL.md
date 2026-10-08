---
name: code-reader
description: Turns a pasted code section into a plain list of the requirements it contains, with triggers, exceptions, and cross-references. Use when someone says 'what does this section actually require', 'break down this code text', or 'pull out the shall statements'.
---
# Code Reader
Produces a numbered list of discrete requirements from a code section, each tied to its exact wording. A good result lets a colleague who never opened the code book know what must be done, when, and what exceptions exist.
## Ask first
1. Paste the section text (including any exceptions and referenced definitions). If you only have a section number, I will look it up in the adopted edition from an official source, or mark it unverified. [paste text]
2. Which edition and jurisdiction adopted it, including local amendments? [unknown; flagged as a gap]
3. What is the project use and size? This lets me mark which requirements are likely in play. [skip; list all]
## Core rules
- Quote the operative words for every requirement; paraphrase alone hides what the code says and invites misreading.
- Split compound sentences into one requirement per line because each one can have a different trigger.
- Record exceptions next to the rule they modify, since an exception usually changes the answer.
- Never fill in a number, table value, or section reference that is not in the supplied text. Mark it unverified.
- This is a review aid for a licensed professional, not a compliance determination.
## Workflow
1. Read the whole section and note the defined terms it leans on; ask for definitions you do not have.
2. Extract each requirement: who or what it applies to, the condition that triggers it, the obligation, and any measurable limit.
3. Attach exceptions and 'where permitted by' clauses to their parent requirement.
4. List cross-references the section points to, as items to fetch rather than guess.
5. Output a table: No. | Requirement in plain words | Trigger | Limit as written | Exceptions | Quote location.
## If your setup is different
- No text supplied: ask for it, or fetch from an official source and cite the URL and retrieval date.
- Local amendments exist: treat the amended text as governing and show the difference from the model code.
- Section is from a non-US code: keep that code's terms rather than translating to US terms.
## Check the result
- [ ] Every row traces to a quoted phrase in the supplied text.
- [ ] All exceptions and cross-references are captured or listed as open.
- [ ] No value appears that the source text did not contain.
