---
name: cost-reader
description: Reads a construction cost estimate or budget document and lists what is excluded, assumed, or allowed for. Use when someone asks what is not included in this estimate, what are the assumptions, or is this number complete.
---
# Cost Reader
Produces a plain-language list of exclusions, assumptions, allowances, and qualifications in a cost document. A good result shows what the number really covers and what could add cost later.
## Ask first
1. What kind of document is it (conceptual estimate, GMP, lump-sum, budget)? [ask the user if unclear]
2. What drawing phase was it priced from? [unknown; flag it]
3. Is there a prior estimate to compare? If so, ask for it.
## Core rules
- Quote the exact line or clause; an exclusion's wording decides who pays.
- Treat 'by others', 'by owner', 'allowance', and 'TBD' as open cost, not as included.
- Do not invent unit rates or totals; only report numbers printed in the document.
- Note the pricing date; costs shift over time and the estimate may be stale.
## Workflow
1. Find the basis-of-estimate, qualifications, clarifications, and exclusions sections; note page numbers.
2. List every exclusion in a table: item, quoted wording, page.
3. List assumptions (design level, site conditions, schedule, escalation) with quotes.
4. List allowances with amount and what they are meant to cover.
5. Compare against the drawings or scope the user supplies and flag scope with no price line.
6. Output: three tables (exclusions, assumptions, allowances) plus a short list of 'questions to ask the estimator'.
## If your setup is different
- If no basis section exists, say so and treat that as the first finding.
- If the document is a bid tabulation, hand off to Bid Review for contractor comparison.
- If the currency or region is unclear, ask before comparing figures.
## Check the result
- [ ] Each item quotes the source with a page reference.
- [ ] No numbers appear that are not in the document.
- [ ] Missing sections are reported as missing, not assumed.
