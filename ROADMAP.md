# Roadmap: first six months

<!-- BEGIN company:role -->
emnify GTM Engineer (Senior (IC4), Sales Operations), reports to the Revenue Operations Lead, works with the CRO. Job 5004134101, posted 2026-10-13.
<!-- END company:role -->

This is a plan to be argued with, not a promise. Targets are set with the Revenue Operations Lead in week two, from emnify's own data. No target below is a number yet, on purpose. Everything marked hypothesis: validate is a guess about emnify that week one exists to test.

The posting says the role owns the outbound engine and data enrichment infrastructure, is measured on revenue outcomes, and is expected to ship before the plan is perfect. The plan is built around those three.

## Weeks 1-4: listen, audit, ship one small thing

| Week | Do | Done when |
|---|---|---|
| 1 | Walk through the current Clay tables, Salesforce account and lead fields, n8n workflows, Amplemarket sequences, Attention and Weflow setup with whoever built them. Read the last two quarters of pipeline | I can draw the data flow and name its owner at each step |
| 2 | Agree with the Revenue Operations Lead: the revenue metric I am measured on, the first target, and what I may write to Salesforce without review | One page, signed off, in [knowledge/definitions](knowledge/definitions/revenue-metrics.yaml) |
| 2-3 | Audit enrichment: fill rate, wrong-field rate and duplicates per field and provider, on a hand-labelled sample | A table of credits per correct field by provider |
| 3-4 | **Ship:** one enrichment run on a small, real list, dry-run first, human approval on every write, using the rules in [enrichment/](enrichment/README.md) | Records in Salesforce that a rep confirms are better than before, and a log of what changed |

Not in this window: new vendors, new agents, anything sent to prospects.

## Months 2-3: outbound engine v1

| Do | Done when |
|---|---|
| Replace hypothesis weights in [scoring](outbound/scoring_weights.yaml) with ones calibrated on emnify's won and lost accounts | Ranking explains last year's wins better than a firmographic sort does, shown on held-out accounts |
| Run the consumption [coverage model](outbound/coverage.py) on real pipeline and real go-live history | The model's assumptions are replaced by measured ramp and realization, and the RevOps Lead trusts the output enough to use it in a forecast conversation |
| Turn the agreed contracts in [knowledge/](knowledge/README.md) into live n8n workflows, still approval-gated | Every write path has a contract, an owner and a kill switch |
| Launch one outbound motion for one vertical from [ICP.md](ICP.md) through Amplemarket | Pipeline created per 100 accounts worked, measured against the previous motion |
| Add the qualification fields from [consumption-qualification](knowledge/process/consumption-qualification.yaml) to opportunities | Field completeness at stage two is reported weekly |

## Months 4-6: measure and earn autonomy

| Do | Done when |
|---|---|
| Compare cohorts: pipeline created and win rate for signal-triggered versus list-based outbound | A written result with the sample size, including if the result is null |
| Compare expected and realized usage for closed-won cohorts ([usage_realization](knowledge/definitions/revenue-metrics.yaml)) | The forecast model is corrected or confirmed with evidence |
| Review agent outputs against [the rubric](agents/evals/RUBRIC.md); move a task from full review to spot-check only where the evidence supports it | One task moved, with the audit trail, or a written reason none did |
| Decide what to cut | A stack and workflow list shorter than at the start, or a reason it is not |

Regions in scope for first motions: <!-- BEGIN company:regions -->
EMEA, NA, APAC (hypothesis: validate)
<!-- END company:regions -->

## What would make me change this plan

- The data audit shows enrichment is already good: move effort to routing speed and signal capture.
- Revenue is concentrated in a vertical not on the list: re-order [ICP.md](ICP.md) before building anything for the others.
- There is no usable history of device counts or go-live dates: the first project becomes capturing it.
