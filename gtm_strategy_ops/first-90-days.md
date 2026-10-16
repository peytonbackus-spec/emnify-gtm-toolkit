# First 90 Days: GTM Strategy & Operations Manager

![Strategy & Ops](https://img.shields.io/badge/role-GTM%20Strategy%20%26%20Ops-2DA44E)

Principle: **the forecast is the product.** Every change in days 31–90 has to make the weekly forecast call more accurate or faster.

## Days 1–30: Audit and baseline

| Week | Focus | Output |
|---|---|---|
| 1 | Sit in every forecast call (manager and leadership). Meet Sales, Finance/FP&A and CS leaders. | How the forecast is built today, step by step; the top 5 pains |
| 1–2 | Run the [DQ monitor](../shared_core/data_quality/dq_monitor.py) opportunity rules against the live CRM. Reconcile [FORECAST_TOOL] ↔ Salesforce totals by category. | Opportunity DQ baseline; sync gaps |
| 2–3 | Pull the last 4 quarters of [FORECAST_TOOL] snapshots. Compute week-4, 8 and 12 accuracy and bias by region ([method](forecasting/forecast_accuracy.py)). | Accuracy baseline; bias pattern by region |
| 3 | Review stage definitions against how deals actually move: time in stage, skipped stages, Commit in early stages. | Gap list against the [target stage design](opportunity_lifecycle/stage-definitions.md) |
| 1 | Hold the [VP of Sales intake](sales_leadership/vp-intake.md) 1:1: snapshot or full, cadence, definitions. | Agreed brief format; first weekly [brief](sales_leadership/vp_brief.py) by week 3 |
| 4 | Renewal book review with CS: next 180 days of renewals, health inputs available, churn reasons from the last 4 quarters. | First renewal-risk list; data available for the health model |

## Days 31–60: Fix the foundation

- Agree stage exit criteria with sales leadership. Ship them as validation rules (EB required at stage 4, no Commit before stage 5 without approval).
- Split forecasts in [FORECAST_TOOL]: new business / renewals / product line / partner.
- Make closed-lost and churn reasons required, with the [taxonomy](renewals/closed-lost-and-churn-taxonomy.md). Run the first monthly loss review.
- Formalize the partner-sourced workflow (deal registration, conflict rule, attribution) with the channel lead.
- Turn on field history for StageName and CloseDate. Run [stage velocity](sales_leadership/stage_velocity.py) and the [deal board](sales_leadership/deal_board.py) before every forecast call.

## Days 61–90: First AI workflow in the forecast

- **Deal-risk flags + forecast commentary:** shadow mode for 2 forecast cycles, then shown to managers before the forecast calls. Every flag goes through HITL. Track the % of flags managers agree with.
- **Renewal health v1** live for the T-180 window, with AI briefs for At Risk accounts routed to CS and AE.
- **Planning for next year:** [capacity and hiring plan, quota vs capacity, territory balance](sales_planning/README.md) on real productivity and ramp history, before the planning cycle starts.
- Day 90 readout: the accuracy baseline vs current; flag precision; manager prep time; renewal risk caught early.

## Questions to ask in week one

1. What was week-8 commit accuracy last quarter, and does anyone track it today?
2. Are renewals forecast in the same [FORECAST_TOOL] forecast as new business?
3. Which usage data reaches the CRM or the warehouse, and how fresh is it?
4. How do Finance and Sales reconcile bookings vs revenue for each deal type?
5. Who owns [FORECAST_TOOL] admin today, and what's the [CONVERSATION_INTELLIGENCE] adoption rate?
6. Has the go-to-market org recently changed (new leadership, merged teams)? What does leadership want the forecast and QBR rhythm to look like, and which of today's processes are already marked for change?
