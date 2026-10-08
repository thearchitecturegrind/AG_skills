---
name: cite-check
description: Verifies that a code or standard citation is real, says what the writer claims, and is the current adopted edition. Use when you have a reference on a drawing, in a letter, or in a consultant report and want it checked before you rely on it.
---
# Cite Check
Produces a verdict for each citation: confirmed, wrong, outdated, or unverifiable, with the official source checked. A good result protects you from carrying a mistyped or superseded section number into a submittal.
## Ask first
1. List the citations and the claim each one supports (section, edition, jurisdiction). [required]
2. Where did the citation come from, such as a past project, a consultant, or a template? Copied citations are the likeliest to be stale. [unknown]
3. Which edition is adopted on this project? If unknown, I will find the adopting ordinance. [find it]
## Core rules
- Check the citation against an official or publisher source, not a forum or summary, because secondary sources repeat errors.
- Compare the cited text with the claim; a real section can still not say what the writer says.
- Confirm the edition currently adopted and any later amendments; the model code's newest edition is often not the enforced one.
- Record the source URL and date checked for every verdict.
- If no official source is reachable, say unverifiable. Do not infer from memory.
## Workflow
1. Normalize each citation into code, edition, section, and the claimed requirement.
2. Look up the section in the adopted edition and compare the actual wording to the claim.
3. Check whether the edition and section are still the current adopted ones, including renumbering.
4. Assign a verdict and, where wrong, propose the corrected citation with source.
5. Output a table: Citation as written | Verdict | What the source says | Source and date | Fix.
## If your setup is different
- Only a section number was given: verify it exists, but flag that the claim cannot be judged without the claim text.
- Source is behind a paywall: ask the user to paste the text or use the publisher's free-view access.
- Different country or standards body: apply the same method with that body's official site.
## Check the result
- [ ] Every verdict has a source and retrieval date.
- [ ] Claim and text were compared, not just the number.
- [ ] Unverifiable items are labelled as such.
