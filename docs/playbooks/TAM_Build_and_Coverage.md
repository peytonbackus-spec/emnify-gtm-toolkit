---
type: area
category: revops
tags:
  - area
  - tam
  - coverage
  - account-universe
status: active
last_updated: 2026-10-13
---

# TAM Build and Coverage

Module: `gtm_strategy_ops/sales_planning`. Feeds [`territory_plan.py`](../../gtm_strategy_ops/sales_planning/territory_plan.py) (account universe) and the market check in [Annual Plan Versioning](Annual_Plan_Versioning_and_Reforecast.md).

## Executive Summary

Build TAM as an enumerated, deduplicated list of companies with provenance on every field. Report three scenarios instead of one precise-looking number. Then measure CRM coverage against the same ICP, and fill the gap in small, approved batches.

## 1. Freeze the definition before counting

- Write the inclusion and exclusion rules first: industry, size, geography, business model, operating conditions, disqualifiers. Mark which filters each source can actually apply.
- The unit is the company, not the person. Decide in advance how subsidiaries, franchises, agencies and parent groups count, and keep one canonical domain per operating account.

## 2. Build the universe to saturation

- **Companies only at this stage.** Contact enrichment and email verification are a later, separate stage that's priced per contact, so don't pay for them on companies you haven't qualified.
- **Retrieve, don't infer.** Never guess headcount from how a website looks or geography from a top-level domain. Every field records its source and confidence.
- **Deduplicate on root domain,** never on company name.
- **Keep querying new sources and variants** until each query adds almost no new domains, and log that curve. Any cap (top-N, budget, rate limit) is stated in the output.
- **A provider's result cap is a floor, not the market.**

## 3. Three scenarios

| Scenario | Definition |
|---|---|
| Low | Verified eligible accounts after known exclusions |
| Base | Verified count adjusted for measured source coverage and overlap |
| High | Base plus populations hidden by caps or filters a source can't apply |

For each scenario, calculate:
- **Revenue TAM** = accounts × ACV. ACV is the median annualized closed-won value in the closest segment. With fewer than 20 comparable deals, show the sample size and a ±25% sensitivity. Never use the top price on the pricing page.
- **Contact target** = accounts × required buying roles.

Report the verified core and the unknown-size tier as separate numbers.

## 4. Measure coverage honestly

Classify every CRM account as in-TAM, out-of-TAM or unknown, against the same ICP. Only verified in-TAM accounts count as coverage. Report account coverage, contact coverage and role coverage (required role slots filled) separately.

Worked example from the source:
- **Universe:** a 40,000 cap from one source, plus 8,500 from a second with 2,000 overlap, gives a base of at least 46,500.
- **CRM:** 19,000 accounts, of which 11,500 are in-TAM.
- **Coverage:** 24.7%, not the 40.9% you get by counting every CRM record.
- **When the CRM out-counts the estimate:** if verified in-TAM accounts later exceed the estimate, raise the estimate. Never report coverage above 100%.

## 5. Fill the gap in governed batches

- Prioritize uncovered accounts by ICP strength and evidence quality.
- Resolve identity before creating anything (the global `crm-enrichment-sync` skill includes the resolve-before-create gate).
- Each proposed account carries its source, domain, fit evidence, owner and acquisition cost.
- Sample quality and cost before buying; record creation needs approval.
- Track attempted, resolved, created, rejected and ambiguous records.

## 6. Burn-up

Take dated coverage snapshots using the same definitions. Show losses from deduplication, disqualification and stale contacts. Don't project a time-to-target from fewer than three comparable snapshots.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/ryan-iyengar/build-and-fill-a-tam` and `skills/tanyo-gochev/tam-builder` (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._
