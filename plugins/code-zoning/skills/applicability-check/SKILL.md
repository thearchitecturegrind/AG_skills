---
name: applicability-check
description: Decides whether a specific requirement applies to a specific project, showing the conditions that must be true and which are confirmed. Use when asked 'does this apply to us', 'is this triggered', or 'do we need to comply with this'.
---
# Applicability Check
Produces an applies / does not apply / depends verdict for one requirement against project facts, with each condition listed. A good result names the single missing fact that would settle an uncertain answer.
## Ask first
1. What is the requirement? Paste its text, or give the section and I will fetch it from an official source. [paste text]
2. Project facts: use or occupancy, size, number of stories, new construction vs alteration vs change of use, and location. [list what you know]
3. Is the building existing? Existing-building provisions often change thresholds. [assume new; say so]
## Core rules
- Break the requirement into its trigger conditions first; applicability is the AND/OR of those conditions, not a gut call.
- Mark each project fact as confirmed (with source), assumed, or unknown, because an assumption silently carried forward becomes a wrong answer.
- Check exceptions and scope statements, since they can remove a requirement the trigger would catch.
- Take thresholds only from supplied or officially sourced text; none from memory.
- A 'depends' result must name the exact fact needed. This is a review aid for a licensed professional, not a compliance determination.
## Workflow
1. Restate the requirement and list every condition that must hold for it to apply.
2. Test each condition against the project facts and tag it met, not met, or unknown.
3. Review scope sentences, exceptions, and alteration or change-of-use clauses for outs.
4. Give the verdict and the reasoning chain in two or three sentences.
5. Output: Verdict | Condition table (condition, project fact, source, status) | Missing facts | Who to confirm with.
## If your setup is different
- Facts are incomplete: deliver a conditional verdict and the question list rather than guessing.
- A local amendment changes the trigger: apply the amended wording and note the difference.
- Authority has issued an interpretation: cite it and let it override your reading, noting its date.
## Check the result
- [ ] Each condition has a status and a source.
- [ ] The verdict follows from the table, not the other way round.
- [ ] Unknowns are listed as questions with an owner.
