---
type: area
category: revops
tags:
  - area
  - revenue-planning
  - reforecast
  - fpa
status: active
last_updated: 2026-10-13
---

# Annual Plan Versioning and Reforecast Triggers

Module: `gtm_strategy_ops/sales_planning`. The capacity math stays in [`capacity_plan.py`](../../gtm_strategy_ops/sales_planning/capacity_plan.py) and [`quota_plan.py`](../../gtm_strategy_ops/sales_planning/quota_plan.py) (decision #20). This playbook governs the plan *around* those numbers: versions, reconciliation and when a reforecast is allowed.

## Executive Summary

Build the plan bottoms-up first, then reconcile it with Finance's top-down target using named scenarios that each have an owner. Keep every version. Reforecast only when a pre-agreed trigger fires.

## Three questions, three analyses

Keep these separate:

1. **What can we produce?** Capacity and known pipeline (bottoms-up).
2. **What do we want?** The strategic target (top-down).
3. **What will the market allow?** ICP sizing; see [TAM Build and Coverage](TAM_Build_and_Coverage.md).

Blending them produces noise.

## Bottoms-up, by revenue type

| Revenue type | Base formula | Predictability |
|---|---|---|
| New business | Capacity (RREs × productivity), capped by available pipeline, then haircut for slippage | Lowest |
| Expansion | Expansion base × gross retention × (1 + net expansion rate) | Medium |
| Renewal | Renewal base × GRR, minus at-risk accounts, plus expected saves | Highest |

Put every assumption in one sheet with its value, source, owner and confidence. That sheet is the contract between Revenue and Finance, and it locks at the end of the bottoms-up phase.

## Reconciliation (one meeting, about 90 minutes)

1. **Frame it as a diagnosis, not a negotiation.**
2. **Bottoms-up** by segment, with its risks.
3. **Top-down** target, drivers and sensitivity.
4. **Close the gap with named scenarios.** For example: an earlier hire, a CS expansion program, ABM pipeline investment. Each scenario gets an owner, its assumptions, its dependencies, its cost and **the year the money lands**.
5. **Lock the plan of record,** with the scenarios listed separately from the base.

Never spread a gap evenly across teams: it destroys accountability and invites sandbagging. If scenarios can't close the gap, the CEO decides. Don't let the debate run on.

## Three versions, all kept

| Version | Owner | Locked when | Purpose |
|---|---|---|---|
| Bottoms-up original (BO) | VP Sales and RevOps | After reconciliation | Shows whether capacity held up |
| Finance stretch (FS) | CFO | After reconciliation | Comparison baseline |
| Plan of record (POR) | CEO, CFO and VP Sales | Board approval | The one number everyone executes |

Every reforecast is a new dated file that compares the current forecast against **both** POR and BO:

- **Below POR but near BO:** execution is fine; the stretch scenarios aren't landing.
- **Below BO:** capacity or a core assumption broke.

## Reforecast triggers (house defaults, set jointly and locked for the year)

| Category | Trigger | Response window |
|---|---|---|
| Pipeline | Coverage below 2.5x (below 2.0x is critical) | 2 days to escalate; 5 to reforecast |
| Execution | Variance from POR above 15% for 2 consecutive periods; a hire missed by its planned month | 5 days |
| Forecast quality | Accuracy outside ±20% for 2 consecutive months; more than half of named deals slip | 3-5 days |
| Unit economics | NRR below 105% for 2 consecutive quarters; CAC payback above 14 months; gross margin more than 3 points under plan | 5 days |
| External | A competitor wins 3+ of our bids in a month; a dependent product release slips 6+ weeks; a macro shock | 2-5 days |

Several triggers firing at once lead to one combined reforecast, not several small ones.

**Locked mid-year:** quotas, the headcount plan, comp structure and the ICP definition. **Flexible:** the revenue forecast, pipeline assumptions and scenario owners.

## Rhythm

- **Weekly:** a 30-minute RevOps and FP&A sync for signals only, no decisions.
- **Monthly:** forecast vs POR review.
- **Quarterly:** a full reforecast that resets assumptions against BO and FS.

## Year-end assumption audit

Table each assumption against its actual and its dollar impact, find the root cause, and carry the corrected value into next year's bottoms-up. A miss you can't trace to an assumption hasn't taught you anything yet.

## What we did not adopt

- **The source's workbook generator:** its formulas are broken and `capacity_plan.py` already covers it.
- **Its quoted market benchmarks:** they go to the GTM 2nd Brain register.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/rutger-katz/revops-revenue-planning` (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._
