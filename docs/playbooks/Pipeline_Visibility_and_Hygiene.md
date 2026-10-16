---
type: area
category: revops
tags:
  - area
  - pipeline
  - hygiene
  - dashboards
status: active
last_updated: 2026-10-13
---

# Pipeline Visibility and Hygiene

Module: `gtm_strategy_ops/pipeline_analytics`. Extends [dashboard-spec.md](../../gtm_strategy_ops/pipeline_analytics/dashboard-spec.md) and [`pipeline_report.py`](../../gtm_strategy_ops/pipeline_analytics/pipeline_report.py).

## Executive Summary

Having dashboards is not the same as having visibility. Visibility needs four layers, and most teams stop after the second:

1. **Structure:** stages with checkable exit criteria.
2. **Reporting:** what the pipeline looks like.
3. **Hygiene:** rules that keep the data true.
4. **Intelligence:** signals that surface what needs attention this week.

This playbook covers layers 1, 3 and 4. The dashboard spec already covers layer 2.

## Layer 1: stage structure

- **Stages describe what the buyer did,** not what the seller did. Keep to five to eight.
- **Every stage has a verifiable exit criterion.** "Rep feels good" is not one.
- **Probabilities rise monotonically with stage.** Replace default probabilities with your own stage-to-close rates from the last 12 months of closed deals within 90 days of go-live, then re-check quarterly. Stage definitions live in [stage-definitions.md](../../gtm_strategy_ops/opportunity_lifecycle/stage-definitions.md).

## Layer 3: hygiene rules

| Rule | Starting threshold (practice-based, calibrate to cycle length) | Action |
|---|---|---|
| Stale deal | No activity: Discovery 7d, Qualification 10d, Solution 14d, Proposal 7d, Negotiation 5d | Flag. Task for the owner; the manager is copied from Qualification onward. Escalate at 2x the threshold. |
| Overdue close date | Close date before today on an open deal | Create an owner task with the last meaningful activity. **Never auto-push the date**: an invented date is a forecast error that looks like clean data. Track a push count per deal. |
| Close date pushed 3+ times | Push count ≥ 3 | Flag for the next pipeline review: the timeline isn't real. |
| Single-threaded late stage | One contact at Proposal or later | Multi-threading task. |
| Placeholder or zero amount | Amount empty or 0 at Proposal or later | Owner task. |

Target: less than 5% of open pipeline with an overdue close date.

Every hygiene write (flags, tasks) goes through [`hitl.py`](../../shared_core/ai_governance/hitl.py). Field corrections go through the [CRM cleanup contract](../contracts/crm-cleanup-contract.md).

## Layer 4: signals that predict outcomes

| Signal | Reading | Response |
|---|---|---|
| No activity for 7+ days at Proposal or later | At risk | Manager checks with the champion |
| Amount decreased | Scope shrink or competitive pressure | Win-strategy review |
| Stage regression | Qualification lost | Re-qualify or close |
| Champion gone quiet | Organizational change | Executive-sponsor outreach |
| New competitor in notes | Competitive threat | Positioning resources |
| Buyer activity spike | Evaluation intensifying | Make sure resources are available |

## The weekly pipeline waterfall

Report movement, not just state: starting pipeline, plus created, advanced, minus pushed, lost and won, equals ending pipeline. Reviewed weekly, this answers more forecast questions than any static snapshot.

## Deal quality score (dimensions only)

Score each open deal on six dimensions. The weights are ours to calibrate; the source's research-backed weights are not reused here.

1. Engagement recency and frequency.
2. Number of contacts across functions.
3. Decision-maker access.
4. Time in stage vs that stage's historical median.
5. A specific next step with a date.
6. Trend direction.

Flag any deal declining on two or more dimensions at once.

## What we did not adopt

The source cites coverage and win-rate benchmarks (Clari, Ebsta, Gong) and AI-platform pricing. Per decision #17, those live in the GTM 2nd Brain benchmark register, not here.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/rutger-katz/pipeline-visibility` (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._
