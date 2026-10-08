---
name: test-fit
description: Calculates what fits on a site within your limits, such as setbacks, height, coverage, and floor area ratio. Use when someone says "what can I build here", "test fit the site", "does the programme fit the lot", or "buildable envelope".
---
# Test Fit
Works out the buildable envelope and the floor area that fits within the limits the user supplies, and compares it with the programme. A good result shows each step of the arithmetic and ends in pass, fail, marginal, or cannot-tell.

## Ask first
1. What are the site dimensions or area, and what limits apply (setbacks, height, coverage, floor area ratio, parking)? [supply the zoning text; otherwise I look up the official source and label figures I cannot confirm "unverified"]
2. What is the programme you want to fit? [ask for areas, storeys, and parking needs]
3. Are there easements, trees, slopes, or neighbours that further limit the site? [assume none, and say so]

## Core rules
- Limits come from the user's document or a current official source with date and link; never from memory, because zoning differs by parcel and changes.
- Check how each measure is defined (for example what counts as floor area or height) before calculating.
- Apply the most restrictive limit at each step and say which one governs.
- Show the arithmetic line by line so a planner can check it.
- This is a feasibility aid; the planning authority and the licensed professional confirm.

## Workflow
1. Record site area and shape and each limit with its source.
2. Compute the buildable footprint after setbacks; show dimensions.
3. Compute the maximum footprint under coverage and the maximum floor area under the ratio.
4. Compute the storeys allowed by height, using floor-to-floor heights you state.
5. Take the least of the capacity figures and compare with the programme, including parking.
6. Output: limits table with sources, step-by-step calculation, governing limit, verdict with margin, and what to ask the authority.

## If your setup is different
- Irregular site: ask for coordinates or a survey; approximate by shapes and mark the error.
- Form-based or overlay codes: ask for the controlling plan and work from it.
- Bonus or exceptions: only include them if the user supplies the rule.

## Check the result
- [ ] Each limit has a source and date.
- [ ] The governing limit is named.
- [ ] A verdict is given with numbers.
