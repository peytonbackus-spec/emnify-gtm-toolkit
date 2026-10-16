# First 90 Days: GTM Engineer

![GTM Engineer](https://img.shields.io/badge/role-GTM%20Engineer-1F6FEB)

Principle: **measure before building.** Every change in days 31–90 has a baseline captured in days 1–30.

## Days 1–30: Audit and baseline

| Week | Focus | Output |
|---|---|---|
| 1 | Meet Marketing, SDR leadership, AEs, GTM Systems. Shadow SDR call blocks. | Stakeholder map; top 5 pains, in their words |
| 1–2 | Run the [data-quality monitor](../shared_core/data_quality/dq_monitor.py) against the live CRM (read-only). | Lead and opportunity DQ baseline by rule |
| 2 | Map the current lead lifecycle as it *actually* runs: statuses, routing, Flows, enrichment tables, [SEQUENCER] enrollment. | As-is diagram plus gaps against the [target spec](lead_lifecycle/lead-lifecycle-spec.md) |
| 3 | Baseline the funnel: conversion by source and segment, speed-to-lead, MQL→SAL SLA. | First version of the [funnel dashboard](funnel_analytics/dashboard-spec.md) |
| 4 | Back-test the current lead score against 12 months of outcomes ([calibration method](lead_scoring/calibrate_scoring.py)). | Is the score monotonic? Which segments are mis-weighted? |

## Days 31–60: Fix the foundation

- Agree the **SQL qualification standard** with Marketing, SDR and AE leads. Ship it as required fields and validation rules.
- Ship **routing v2** (rules R1–R7, with reasons stamped on the record), replay-tested in a sandbox against the last 200 MQLs.
- Re-weight scoring from the back-test. Turn on the two-axis grade (fit × intent).
- Tune the enrichment waterfall so paid contact data only runs on B+ fit economic-buyer personas. Report credit spend per pipeline $.
- Agree the line with Marketing Ops: [who owns what](marketing_ops/README.md#who-owns-what), campaign naming and UTM standards ([spec](marketing_ops/campaign-operations-spec.md)), and one [request queue](../gtm_strategy_ops/sales_planning/crm-request-intake.md) for [CRM] and [MARKETING_AUTOMATION] changes.

## Days 61–90: First AI workflow in production

- **Account research brief** for SDRs: shadow mode for 2 weeks, then assisted. Eval set in CI, with the HITL acceptance rate tracked.
- Baselines already captured: SDR research minutes per account, MQL→SQL conversion, speed-to-lead.
- **Demand plan** with Marketing: source mix and leads-by-channel targets for next quarter ([demand plan](marketing_ops/demand_plan.py)).
- Day 90 readout: realized gains against those baselines, and the next two workflows prioritized (qualification assist, routing exceptions).

## Questions to ask in week one

1. Where does the lead score live today, and when was it last validated against closed-won?
2. Which routing exceptions do SDR managers fix by hand every week?
3. How are partner-sourced leads attributed today?
4. Is there a warehouse with the CRM synced, or is reporting CRM-native only?
5. What is the policy on sending prospect data to AI vendors, and who in security signs off?
6. Which lead-side changes are already on the sales leader's list (routing across direct vs channel, SDR structure, tooling)?
