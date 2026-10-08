---
name: compliance-check
description: Checks a drawing or plan, item by item, against code text the user pastes, listing what complies, what does not, and what cannot be told from the drawing. Use when asked 'does this plan meet this section' or 'check my drawing against this text'.
---
# Compliance Check
Produces an item-by-item table pairing each requirement in the pasted text with what the drawing shows. A good result separates real conflicts from things the drawing simply does not show.
## Ask first
1. Paste the code text to check against, and tell me the edition. Without pasted text I will look it up from an official source and label what I could not verify. [required]
2. Attach or describe the drawing, with sheet numbers and scale. [required]
3. Which area of the plan should I focus on? [whole sheet]
## Core rules
- Only judge against the text supplied; adding requirements from memory defeats the point of a traceable check.
- Measure from stated dimensions or a known scale; if the scale is unclear, say cannot-tell instead of eyeballing.
- Use four outcomes: complies, does not comply, marginal, cannot tell; forcing pass or fail hides missing information.
- Cite the drawing location for each finding so the team can verify it.
- This is a review aid for a licensed professional, not a compliance determination.
## Workflow
1. Break the pasted text into individual checkable items.
2. For each item, find the relevant dimension, note, or element on the drawing and record the value read.
3. Compare with the limit in the text, showing the arithmetic.
4. Assign an outcome and note what information would resolve any cannot-tell.
5. Output: Item | Text says | Drawing shows (sheet, location) | Outcome | Action.
## If your setup is different
- Drawing is a sketch without dimensions: limit the check to what can be read and list needed dimensions.
- The text has exceptions you cannot evaluate: mark them as open instead of assuming they apply.
- Drawing uses metric and code uses imperial, or the reverse: convert, show the conversion, and flag rounding.
## Check the result
- [ ] Every outcome cites both the text and the drawing.
- [ ] Cannot-tell items come with the missing input.
- [ ] Arithmetic is shown, not just the result.
