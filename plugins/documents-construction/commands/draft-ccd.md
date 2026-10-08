---
description: Drafts a construction change directive for a change before cost and time are agreed.
argument-hint: [describe the change, reason, sheets affected, and any known pricing status]
---
Draft a construction change directive (CCD) for $ARGUMENTS. A CCD tells the contractor to proceed with a change while cost and time are still unsettled.
If $ARGUMENTS is empty, ask what change, why, which documents, and the contract clause that allows directives.
1. Number placeholder, date, project, to, from.
2. Description of the change with sheet and section citations.
3. Direction to proceed, and the basis for adjustment left open: say that cost and time will be determined under the contract's procedure. Use the clause the user provides; otherwise leave [contract clause].
4. Request for the contractor's cost and time records or proposal, with a response date from the user.
5. Signature blocks for owner and architect as the contract requires.
Mark the output 'DRAFT for review and signature by a licensed professional' at the top. It must not commit the firm to cost, time, or scope; where those are open, say they are reserved.
Output: the directive text and notes on what the reviewer must confirm (authority to direct, notice rules).
