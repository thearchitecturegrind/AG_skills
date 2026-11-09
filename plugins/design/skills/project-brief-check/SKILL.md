---
name: project-brief-check
description: Pressure-tests an architectural project brief, RFP, OPR, or program document before design starts — finds what it never says, what contradicts itself, and what someone will have to decide later at a worse time. Use when the user pastes or attaches a brief, RFP, OPR, program, or scope document and asks whether it's complete, ready, clear, or what's missing; also on "check this brief", "poke holes in this RFP", "what should I ask the client", or "are we ready for SD". Produces a written review plus a ready-to-send list of questions for the owner. Not for critiquing a design, checking drawings, or zoning/code analysis.
---

# Project Brief Check

A brief is a promise the owner makes about what they want. This skill reads that promise like a skeptical project architect on day one: what is actually committed, what is only implied, and what is missing that will cost time or money if nobody asks now.

The deliverable is not a grade. It is a short list of things to resolve and a set of questions the user can paste straight into an email.

## Before you start

Get these, asking only for what you can't find:

1. **The document itself** — pasted, attached, or a file path.
2. **What kind it is** — RFP (selecting a designer), OPR (performance requirements, often for Cx), program (spaces and areas), or design brief (intent and character). The kind changes what "complete" means; see `references/three-reads.md`.
3. **Where the project is**, if the document doesn't say. Never guess a jurisdiction or code edition.
4. **The user's firm benchmarks**, if they want a budget sanity check. Check `references/my-benchmarks.md`; if it's empty, skip the numeric check and say so rather than inventing figures.

If a `docs/project.md` or similar project file exists in the working directory, read it for owner, site, and earlier decisions.

## How to review

Read the document three times, each with a different question in mind. The full prompts are in `references/three-reads.md`.

- **Read for intent** — What is this project *for*? Are the priorities ranked, or is everything equally important (which means nothing is)? Is there a hidden driver — a deadline, a grant, a board, a competitor — that will actually run the job?
- **Read for quantities** — Every number the design will depend on: areas, headcounts, budget, dates, performance targets, code edition. For each: is it stated, is it consistent with the other numbers, and is it plausible?
- **Read for responsibility** — Who decides, who pays, who provides, who is liable. Exclusions, owner-furnished items, existing conditions, surveys, geotech, hazardous materials, approvals and hearings.

Then sort what you found into four buckets:

| Bucket | Meaning |
|---|---|
| **Conflict** | Two statements that cannot both be true. Must be resolved before SD. |
| **Tension** | Goals that compete but can be balanced — name the trade-off, don't resolve it. |
| **Missing** | Something the design will need that the document doesn't give. |
| **Solid** | Parts that are genuinely clear. Say so — it builds trust in the rest. |

Keep it proportionate. A tight two-page program and a 60-page public RFP deserve different lengths of review. Spend words where the risk is.

## Rules

- **Never fill a gap.** If the area, budget, code edition, or authority isn't stated, report it as missing. Don't substitute a "typical" value as if the owner said it.
- **Every finding says why it matters** — what goes wrong, and roughly when (SD, permit, bid, construction), if nobody resolves it.
- **Quote the brief.** When flagging something, cite the clause or page so the user can find it.
- **Separate fact from judgment.** "The brief gives no budget" is fact; "this budget looks low for the region" is judgment and should name the benchmark it's based on.
- **Stay on the brief.** Don't start designing, and don't run zoning or code analysis — recommend it as a next step instead.
- **Don't inflate.** If the brief is good, the review should be short and say so.

## Output

Write the review using `assets/review-template.md`. If the user is working in a project folder, save it as `docs/briefs/YYYY-MM-DD-<short-name>-brief-check.md` (create the folder if needed); otherwise deliver it in chat.

Then tell the user, briefly:
- the two or three things that matter most,
- how many questions are ready to send to the owner,
- what to do next (e.g., zoning study once the parcel is confirmed).
