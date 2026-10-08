---
description: Drafts a certificate of substantial completion and checks its date.
argument-hint: [give project, the claimed date, inspection result, and the punch list status]
---
Draft a certificate of substantial completion from $ARGUMENTS.
If $ARGUMENTS is empty, ask: the contract definition of substantial completion, the claimed date, inspection date and participants, punch list status, and authority approvals obtained.
1. Quote the contract's definition as the user supplies it; do not recall it.
2. Check the claimed date against the evidence (inspection date, approvals, punch status) and say consistent, inconsistent, or cannot tell, showing the dates.
3. Draft the certificate: project, date, scope covered, attached punch list, responsibilities and warranty start left as the contract states.
4. Note effects the contract may attach to the date (warranty, retainage, insurance) as questions, not facts.
Mark the output 'DRAFT for review and signature by a licensed professional' at the top. It must not commit the firm to cost, time, or scope; where those are open, say they are reserved.
Output: the draft certificate and the date check. Signing remains with the architect and owner.
