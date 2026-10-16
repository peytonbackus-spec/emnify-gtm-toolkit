---
type: area
category: revops
tags:
  - area
  - operating-cadence
  - meetings
  - decision-rules
status: active
last_updated: 2026-10-13
---

# Revenue Operating Cadence

Module: `gtm_strategy_ops/sales_leadership`. Works with [forecast-cadence.md](../../gtm_strategy_ops/forecasting/forecast-cadence.md) and the [VP brief](../../gtm_strategy_ops/sales_leadership/README.md).

## Executive Summary

A cadence is the calendar that turns the strategy scorecard and the dashboards into decisions. Without one, meetings become status updates. This playbook covers three things:

- a gate every meeting must pass;
- a lean ritual calendar;
- signal-based rules for which meeting a breached metric escalates to.

## The 5P gate

A meeting runs only if its owner can write down all five:

1. **Purpose:** one sentence ending in an outcome ("we will decide..."), not an activity ("discuss", "review").
2. **Product:** the artifact that proves the time was worth it, such as logged decisions with IDs and owners, an updated forecast, or a ranked problem list.
3. **People:** the smallest set of roles that can produce it. No spectators; invite by role.
4. **Process:** two to five timeboxed agenda items, with named facilitator, decider and note-taker.
5. **Proof:** pre-reads sent a working day ahead, with a baseline so the decision can be judged later.

If any P is missing, cancel the meeting or replace it with an async update. A healthy calendar cancels 5-15% of meetings (practice-based). A 0% cancel rate means the gate isn't enforced.

## Ritual calendar (adapt to company size)

| Rhythm | Ritual | Owner | Product |
|---|---|---|---|
| Daily | Pipeline pulse (15 min, self-serve CRM views) | Sales manager | Blockers cleared |
| Weekly | Revenue review: pipeline and decisions (≤75 min, at most 3 decisions) | CRO | Decision log entries |
| Weekly | Forecast roll-up (30 min) | CRO with RevOps | Locked forecast and gap actions |
| Weekly | Function loops: demand, pipeline, CS value (≤45 min each) | VP per function | Experiments with stop rules; account attention list |
| Weekly | Breach huddle (30 min) | RevOps on call | Owner and containment per SLA breach |
| Biweekly | Demo and retro | Rotating | Keep / kill / scale decisions |
| Monthly | Strategy and lever review (90 min) | CEO and CRO | WIP caps; next levers |
| Monthly | Data and definition review (60 min) | RevOps | Freshness status; definition change log |
| Quarterly | Reset (2-3 h) | CEO | Updated scorecard, targets and SLOs; cadence changes only here |

Design rules:
- Reduce, never add: to add a meeting, cancel one.
- Put decision sessions early in the week.
- Every ritual feeds the same dashboard; no parallel numbers (decision #19).

## Signal-based decision rules

Pick 8-12 signals you already have data for. Set thresholds from about six months of history, and route each breach to one ritual. Examples:

| Signal crosses | Escalates to |
|---|---|
| Segment pipeline coverage below 2.5x for 3 weeks | Demand loop |
| Win rate drops more than 5 points | Pipeline loop (open an A3) |
| Decision latency over 14 days | Strategy and lever review |
| 5P cancel rate at 0% for 4 weeks | Strategy and lever review |

## Cadence health metrics

Review these monthly and change the cadence only at the quarterly reset:

- **Decision latency:** signal to logged decision to live countermeasure; target under 7 days.
- **5P cancel rate.**
- **SLO hit rate.**
- **Data freshness pass rate.**
- **Forecast-in-band rate.**
- **Experiment kill rate:** 20%+ per quarter. Under 10% means stop rules aren't real.
- **Coaching follow-through.**

## Board update: five questions, about ten minutes

1. Are we on track? One number with a trend line.
2. Why? Win rate by segment and motion, plus the top three loss reasons.
3. What changed? Actions taken and their measured effect.
4. What do we need? Each ask tied to a conversion gap.
5. What's the risk? The top three, specifically.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/rutger-katz/operating-cadence-designer` (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._
