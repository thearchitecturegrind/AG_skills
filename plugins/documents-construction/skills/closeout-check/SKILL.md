---
name: closeout-check
description: Tracks closeout deliverables (warranties, manuals, as-builts, attic stock, certificates) from the spec through handover. Use when someone says closeout checklist, what is still owed at closeout, or are we ready to hand over.
---
# Closeout Check
Produces a closeout tracker built from the specification and contract, showing each deliverable's status and who owes it. A good result makes the final handover date realistic.
## Ask first
1. Do you have the spec book and general conditions? [ask; closeout lists live in Division 01 and each section]
2. What jurisdiction's final approvals apply? [ask; look up from the authority, not memory]
3. Who receives the deliverables (owner, facility manager)? [ask]
## Core rules
- Build the list from the project's own documents; requirements differ by project.
- Track receipt and review separately; a document received may still be rejected.
- Warranty start dates follow the contract; quote the clause rather than assuming.
- Certificates and approvals come from authorities; list them as external dependencies.
## Workflow
1. Search the spec for closeout, warranty, operation and maintenance, record document, and attic stock requirements.
2. Create rows: item, spec section, responsible party, due, status.
3. Add authority items (final inspection, occupancy certificate) per the user's jurisdiction.
4. Update status as the user reports; flag overdue and rejected items.
5. Link punch list completion and final payment conditions if the contract states them.
6. Output: tracker table plus a short list of blockers to handover.
## If your setup is different
- If no spec is available, produce a generic request list marked unverified.
- If the project is residential or small, merge categories but keep warranties and as-builts.
- If the owner has own requirements, they override the generic list.
## Check the result
- [ ] Every row cites a spec section or marks itself unverified.
- [ ] Statuses distinguish received from accepted.
- [ ] External approvals are separate from contractor items.
