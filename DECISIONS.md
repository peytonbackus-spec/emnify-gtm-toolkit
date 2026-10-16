# Decision log

Format: decision, why, what would reverse it. Entries 1-9 are choices made in this repo. The push-back examples are illustrations of how I would answer a request I think is the wrong solution; they are not events at emnify.

## Choices in this repo

| # | Decision | Why | Reversed if |
|---|---|---|---|
| 1 | Coverage is measured in realized-in-period usage revenue (low / expected / high), not signed contract value | Consumption revenue ramps after signature, so contract value overstates a period | Real data shows go-live and usage are close to contract value |
| 2 | Clay is specified, not run. No workspace was opened and no credits spent | I do not have access to emnify's Clay, and a demo table would imply data I do not have | I get a sandbox workspace |
| 3 | Writes are dry-run by default and need a named human approver | One wrong bulk write to the system of record costs more than one slow week | An audit shows an error rate low enough to move to exceptions-only |
| 4 | Waterfall conditions are structured data, not evaluated strings | Rules that non-engineers edit must not execute code. The inherited engine uses `eval`; this layer does not | Never |
| 5 | Agents propose; people accept, modify or ignore. Agents never set stage, forecast category or amount | A bad forecast field spreads. Autonomy is earned per task with evidence | Per task, through the earned-autonomy steps in [shared_core](shared_core/ai_governance/earned-autonomy.md) |
| 6 | Every vertical gets the same fit points until win data ranks them | The list comes from the public site, not from emnify's results | Win and loss data exists |
| 7 | Two config files: [company.yaml](company.yaml) for emnify, [config/company.yaml](config/company.yaml) for the inherited demo engines | The inherited engines need segment keys that match their synthetic data; mixing them would put invented segments next to emnify hypotheses | The inherited engines are re-keyed to the emnify verticals |
| 8 | Knowledge is YAML with a schema and a validator, not free-form wiki pages | Agents and people need the same source; a validator catches a stale or incomplete contract | A document type needs prose; then it gets a prose template and the same front matter |
| 9 | The repo is private until I choose to share it | It contains hypotheses about a company I do not work for | I decide to share it |

## Revenue-metric definitions

Defined once in [knowledge/definitions/revenue-metrics.yaml](knowledge/definitions/revenue-metrics.yaml) and proposed to the Revenue Operations Lead. The ones that matter most for consumption revenue:

- **expected usage revenue**: devices x expected monthly data per device x price per unit x months, shaped by the ramp curve, always a range.
- **coverage ratio**: open pipeline in expected-usage terms divided by the remaining target.
- **usage realization**: realized divided by expected, per cohort. It tells us whether the forecast is honest.
- **speed to lead**: minutes from the first qualifying signal to the first human touch.

## Push-back examples (illustrative)

| Request | My response | What I would offer instead |
|---|---|---|
| "Auto-enroll every enriched lead into a sequence." | Enrichment confirms a record exists, not that it fits or wants to hear from us. I have not run auto-enrollment in production, so I would pilot it | Auto-enroll only the top tier, one vertical, with approval on the first batches and a stop rule on bounce and complaint rates. See [outbound-launch](knowledge/process/outbound-launch.yaml) |
| "Add another data vendor; fill rate is low." | Fill rate does not tell me which values are right. A second vendor can add wrong values faster | Measure precision per provider on a labelled sample first, then decide ([precision_audit](gtm_engineer/enrichment/precision_audit.py)) |
| "Score accounts by company size." | Size is a weak proxy when the revenue driver is device count and countries | Score on vertical, signals and expected devices, and flag when devices are unknown ([scoring](outbound/scoring.py)) |
| "Let the agent update the forecast category." | A wrong category moves a number leadership reads | The agent proposes the missing qualification fields; the AE sets the category |
| "Report how many records we enriched." | Records enriched is activity. It can rise while pipeline falls | Report pipeline created per 100 accounts worked, by source, and revenue realized by cohort |
| "Ship the full integration before we start." | A plan that waits for completeness ships nothing | One small, reversible run in week three, then widen |

## Open questions (hypothesis: validate)

- Which fiscal calendar and territory model apply?
- Which Salesforce objects hold device count, countries and go-live?
- Where do Attention call summaries land, and who owns them?
- What is the do-not-contact source of truth?
