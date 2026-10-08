---
description: Calculates required fixture counts from a supplied table.
argument-hint: [paste the fixture table and the occupant load by use]
---
Calculate required plumbing fixtures for: $ARGUMENTS
If $ARGUMENTS is empty, ask for the fixture table (or code and edition so you can fetch it), occupant loads by use, and the male/female split assumption.
Use only table values or code text the user pastes, or ones you fetch from a current official source and cite with URL and date; never use values from memory. If you cannot verify a value, label it unverified.
Steps: (1) set occupant count per use and gender split, stating the assumption; (2) for each fixture type (water closets, lavatories, drinking fountains, service sinks), find the row and ratio; (3) compute the count step by step; (4) round per the table; (5) add accessible fixtures only from supplied text.
Output: a table (Fixture | Ratio | Occupants | Calculation | Required) and the totals by sex or by facility, plus assumptions and missing inputs.
Plan check will verify; this is a calculation aid, not a determination.
If a needed input is missing, do not assume it; list it as a question and give the result as cannot-tell for that part.
Format: a short verdict line first, then a table of Item | Source limit | Your value | Margin | Status, then open questions.
