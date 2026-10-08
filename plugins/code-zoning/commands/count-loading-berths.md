---
description: Calculates required loading berths from a supplied table.
argument-hint: [paste the loading table row and the building area/use]
---
Calculate the required number of loading berths for: $ARGUMENTS
If $ARGUMENTS is empty, ask for the zoning or code loading table (or the district so you can fetch it), the use, and the floor area basis the table uses (gross or net).
Use only table values or code text the user pastes, or ones you fetch from a current official source and cite with URL and date; never use values from memory. If you cannot verify a value, label it unverified.
Steps: (1) identify the table row for the use; (2) confirm the area measure and units match the table; (3) apply the thresholds or ratio step by step, showing the arithmetic; (4) apply the table's rounding rule; (5) note any berth size or exemption text.
Output: required berths as a number, the calculation lines, the source row, and assumptions. If the table has exceptions you cannot evaluate, say cannot-tell and list them.
If a needed input is missing, do not assume it; list it as a question and give the result as cannot-tell for that part.
Format: a short verdict line first, then a table of Item | Source limit | Your value | Margin | Status, then open questions.
