---
description: Explains a code section in plain English.
argument-hint: [paste the code section]
---
Explain this code section in plain English for a non-specialist architect: $ARGUMENTS
If $ARGUMENTS is empty, ask the user to paste the section text, and which code, edition, and jurisdiction it comes from.
Work only from the pasted text. If only a section number was given, fetch the text from a current official source and cite it, or say you could not verify it.
Define each technical term in a few words the first time it appears.
Output: (1) one-sentence summary; (2) what it requires, as short bullets; (3) when it applies and the exceptions; (4) what to check on a drawing; (5) open questions.
Do not add requirements from outside the text. Do not give a compliance verdict. If life safety, structure, or accessibility is involved, note it is an explanation for a licensed professional to confirm.
If a needed input is missing, do not assume it; list it as a question and give the result as cannot-tell for that part.
Format: a short verdict line first, then a table of Item | Source limit | Your value | Margin | Status, then open questions.
