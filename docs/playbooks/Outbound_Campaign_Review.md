---
type: area
category: revops
tags:
  - area
  - outbound
  - campaign-performance
  - benchmarking
status: active
last_updated: 2026-10-13
---

# Outbound Campaign Review

Module: `gtm_engineer/marketing_ops`. Sits alongside [`campaign_report.py`](../../gtm_engineer/marketing_ops/campaign_report.py), which covers channel funnel and attribution. This playbook covers sequence-level outbound: the weekly review, diagnosing an underperforming campaign, judging a number, and challenging a draft before launch.

## Executive Summary

Four rules hold everywhere:
- Lead with the people waiting on a reply.
- Never score thin data.
- Diagnose in a fixed funnel order and prescribe one fix.
- Judge against your own history before any published figure.

## Rules for every number

- **Sample size:** every rate carries its denominator. Below 10 sends a metric gets no status, only "insufficient volume". Apply this per step, not just per campaign.
- **Aggregation:** portfolio rates are summed numerators over summed denominators, never an average of campaign rates.
- **Units:** rates move in percentage points, counts in units. "+5 pts" and "+5%" are different claims.
- **Direction:** for bounce, down is good. An arrow colored the wrong way is worse than no arrow.
- **Deliverability:** if a platform defines delivered as sent minus bounced, "deliverability" is just 100 minus bounce. Track bounce and don't present the other as an inbox-placement measure.

## Weekly review (in this order)

1. **Reply queue first.** Meeting requests, then interested, then neutral; longest-waiting first within each group, and flag anything past about 3 days. Rejections and wrong-fits collapse to a count. Neutral ("not now") is a follow-up date, not a discard.
2. **Correct the classifier in the working view only,** and count the corrections. A classifier that keeps mislabelling one category is a finding. The CRM is never rewritten as a side effect of a report.
3. **Count the week from every reply received,** not from the open queue. A mid-week refresh may only add to the week's counts.
4. **Status by primary channel:** the channel carrying most sends sets the campaign status (co-primary at about 30% share). A weak secondary channel is flagged as "leg to fix". Bounce always counts, regardless of channel, because it damages the domain.
5. **Movement against two baselines:** last week, and the trailing four-week average. On the first run, say "baseline week" instead of showing zero deltas.

Starting zones, to replace with the team's own trailing median once there's history:

| Metric | Good | Floor |
|---|---|---|
| Connection acceptance | 30% | 20% |
| LinkedIn reply | 25% | 15% |
| Email open | 60% | 45% |
| Email reply | 6% | 3% |
| Bounce (lower is better) | 2% | 5%, and sending stops above this |

The bounce row is never replaced by the team's own median: a team running at 9% has a domain problem, not a benchmark. Clicks are shown but never drive status.

## Diagnosing a campaign: one fix at the earliest broken step

Walk the funnel in this order and stop at the first red metric:

1. **Delivery:** bounce, complaints, placement. If this is broken, change nothing else.
2. **Engagement:** connection acceptance, opens, open decay by step. Weak acceptance points at targeting, not copy. Low opens with healthy replies usually means a tracking pixel problem.
3. **Replies:** opens healthy but no replies points at the copy or the offer. Replies healthy but mostly negative points at the segment.
4. **Quality:** positive vs negative vs referral vs "not now". A 12% reply rate that's mostly "remove me" is worse than 4% mostly positive.

Other rules:
- **Replies but no meetings:** check response time first; interest decays in hours.
- **Ignore the break-up step:** it's designed to underperform.
- **Confidence:** a red metric on under about 20 sends at that step is a hypothesis, not a finding.
- **Rank fixes** by severity × people affected.
- **Change one variable at a time,** with a few hundred sends per variant before calling a result.

## Judging a number: name the comparison layer

| Layer | Use |
|---|---|
| External averages | Only to catch something catastrophically wrong; never a target |
| Your own history | Drives decisions |
| Like-for-like in your own book (same offer, different segment, or the reverse) | The only layer that isolates a cause |

Compare only when offer, segment, channel and relationship temperature are held roughly constant. Set targets from your own median (expected case) and best (ceiling), and **write the kill threshold before launch**.

## Challenging a draft before launch

1. Get the whole sequence, plus past campaigns with both their stats **and** their copy. If only stats exist, ask for the copy of the top and bottom performers. Reconstructing structure from a few sent messages is acceptable, if it's labelled.
2. Rank past campaigns on meetings first, replies second. Treat high replies with no meetings as the most interesting row.
3. Compare on things you can point at: number of touches and days end to end, characters per touch, opener type, call to action per touch (and repeats), angle variety, channel order and gaps.
4. Report two readings: what the winners do that the draft doesn't, and what the losers did that the draft repeats.
5. Score copy with the global `reply-pull-gate` skill. Where the team's own winners break a generic rule, the rule loses in that market.
6. Give at most three fixes, each one sentence and each citing the gap behind it. Never edit a live campaign in place: duplicate it and fix the copy.

_Source: adapted in our own words from swan-gtm/gtm-skills `weekly-performance-advisor` and `campaign-challenger` (erwann-lefevre), and `campaign-benchmarking` and `outbound-performance-diagnosis` (tanyo-gochev) (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._
