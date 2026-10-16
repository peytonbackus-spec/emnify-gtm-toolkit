---
type: area
category: revops
tags:
  - area
  - gtm-planning
  - org-design
  - capacity
status: active
last_updated: 2026-10-13
---

# GTM Motion and Org Design

Module: `gtm_strategy_ops/sales_planning`. The territory math stays in [`territory_plan.py`](../../gtm_strategy_ops/sales_planning/territory_plan.py) and [Territory Planning](Territory_Planning_and_Carveout_Model.md); the capacity math in [`capacity_plan.py`](../../gtm_strategy_ops/sales_planning/capacity_plan.py). This playbook covers the decisions that come before those: which motion, which org shape, and when to add either.

## Executive Summary

Choose the motion from ACV, the buyer and how complex the buying decision is. Don't start from the team you want to build. Then size the org from productivity, add specialist roles by ratio, and add a second motion only once the first is repeatable.

## Motion by ACV and buyer (directional bands; validate against your own deal data)

| Motion | ACV (directional) | Typical buyer | Org shape |
|---|---|---|---|
| No-touch / PLG | Under ~$1K | Individual contributor | Product and marketing; no sales team |
| Low-touch | ~$1-10K | Team lead | Inbound response, light qualification |
| Medium-touch | ~$10-50K | Director | SDR to AE handoff, mostly virtual |
| High-touch | ~$50-250K | VP/C-level committee | SDR, AE and SE; territories |
| Dedicated | $250K+ | C-suite, formal procurement | Named-account pod (AE, SE and CSM) |

Two mismatches to watch for:
- **High-touch on a low ACV:** the unit economics fail.
- **Low-touch on a high ACV:** money is left on the table.

Above about $10M ARR, running two or three motions is normal. Keep them operationally separate, with their own funnels and metrics.

## Sequencing rules

1. Prove one motion, document the play, then add the adjacent one. Never launch two new motions at once: you can't learn which one is working.
2. Expand the ICP in phases: one ICP, one geography and one motion first; then new geographies; then new verticals (each needs its own qualification language); then larger accounts (a new motion, not an extension).
3. Plan retention alongside acquisition. At 80% GRR, the business runs to stand still.

## Ratios (practitioner defaults; replace with your own data)

| Ratio | Default range |
|---|---|
| SDR : AE | Inbound-heavy 1:2-3 · balanced 1:1-2 · outbound-heavy 2:1 |
| AE : SE | None for SMB/MM · 3-4:1 for MM/enterprise · 2:1 or 1:1 for strategic |
| CSM coverage | 20-40 accounts (high-touch) · 40-80 (mid) · 100-200+ with automation |
| Manager span | 6-8 SDRs or SMB AEs · 4-6 enterprise AEs · 6-10 CSMs |

AI is moving these ratios: research and personalization are moving back into AE roles, and inbound SDR work is being automated. Revisit the ratios each planning cycle; don't assume today's roles will last.

## When to add leadership roles

- **First RevOps hire:** around $3-5M ARR, or earlier if no one can produce a pipeline report people trust.
- **A CRO over a VP of Sales:** when there are two or more distinct motions, around $15M+ ARR, and sales, CS and partners need one owner. Hiring a CRO too early is expensive.

## Efficiency checks per motion

Each motion has to stand on its own:
- CAC payback under about 12 months for self-serve, 18 for inside sales and 24 for enterprise.
- GRR at or above the motion's floor.
- GTM spend per dollar of net new ARR trending down.

A motion with payback above 24 months **and** GRR below its floor is destroying value even while it adds ARR.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/rutger-katz/gtm-planning` (MIT, © 2026 Swan). Podcast-sourced productivity stats were not carried over. See the [crosswalk](../crosswalks/swan-gtm-skills.md)._
