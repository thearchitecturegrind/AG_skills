---
description: Explains a geotechnical recommendation in plain English.
argument-hint: [paste the recommendation from the soils report]
---
Explain this geotechnical recommendation in plain English: $ARGUMENTS
If $ARGUMENTS is empty, ask for the pasted recommendation, the page number, and the structure type.
Define soil terms in a few words the first time they appear (for example, bearing capacity means the load the ground can carry).
Output: (1) what the engineer is saying; (2) why it matters to the design or construction; (3) who has to act, by role; (4) what it likely costs or delays in general terms without inventing numbers; (5) questions to ask the geotechnical engineer.
Do not recalculate or change values. Structural and foundation decisions belong to licensed engineers; this explains, it does not advise on design.
If a needed input is missing, do not assume it; list it as a question and give the result as cannot-tell for that part.
Format: a short verdict line first, then a table of Item | Source limit | Your value | Margin | Status, then open questions.
