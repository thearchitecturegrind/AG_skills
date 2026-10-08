---
name: schedule-review
description: Reads a contractor's construction schedule and identifies the assumptions it makes about the owner and design team, such as review times and decisions. Use when someone says review the contractor's schedule, what does this schedule assume of us, or can we meet these dates.
---
# Schedule Review
Produces a list of review durations, owner decisions, and design deliverables the schedule depends on. A good result lets the architect object or plan before the schedule becomes a commitment.
## Ask first
1. What format is the schedule (PDF, spreadsheet, export)? [ask]
2. What review times does the contract allow the design team? [ask for the clause]
3. What is the contractual completion date? [ask]
## Core rules
- Compare schedule durations to contract periods the user gives; do not assume standard times.
- Look for hidden dependencies: submittals, owner-furnished items, permits, inspections.
- Check logic around design-team activities, such as shop drawing reviews and RFI answers.
- Report facts and questions; do not accept or reject the schedule.
## Workflow
1. Identify the milestones, completion date, and critical path if shown.
2. List activities owned by the owner or design team with durations.
3. Compare each duration with the contract period supplied.
4. Check procurement of long-lead items against submittal dates.
5. Flag unrealistic overlaps, missing activities (commissioning, inspections), and float use.
6. Output: assumption table (activity, assumed time, contract time, gap) and questions for the contractor.
## If your setup is different
- If only a bar chart image exists, read durations approximately and say so.
- If there is no contract clause, report durations without judgment.
- If it is a recovery schedule, ask what changed from the baseline.
## Check the result
- [ ] Each assumption cites an activity ID or row.
- [ ] Contract periods come from the user.
- [ ] No acceptance is stated.
