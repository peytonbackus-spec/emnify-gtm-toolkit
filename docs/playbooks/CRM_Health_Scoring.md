---
type: area
category: revops
tags:
  - area
  - data-quality
  - crm
  - health-score
status: active
last_updated: 2026-10-13
---

# CRM Health Scoring

Module: `shared_core/data_quality`. Builds on [`dq_monitor.py`](../../shared_core/data_quality/dq_monitor.py), which already reports a pass rate per rule. Corrections go through the [CRM cleanup contract](../contracts/crm-cleanup-contract.md); a health report never authorizes a write.

## Executive Summary

Make "is the CRM getting healthier?" a reproducible number. That means versioned rules, object-level scores, unknowns kept visible, and critical rules that the composite score can never hide.

## Define health as rules

Each rule declares:
- its population;
- its condition;
- its severity (impact weight 1-5);
- its evidence;
- its exclusions;
- its owner.

Cover identity, ownership, critical-field completeness, pipeline integrity, process conformance and integration drift. Only measure fields that drive execution or decisions. Don't reward filling optional fields just because they're easy to count.

## Scoring model

- **Rule pass rate** = 1 - failures / eligible records. Unknowns are excluded from the denominator but reported. Above 10% unknown, the rule is marked low-confidence.
- **Object score** = weighted mean of rule pass rates × 100. Score contacts, accounts, opportunities and activities separately.
- **Composite** = objects weighted by business relevance, not record count. A starting weighting: accounts 30%, contacts 25%, opportunities 35%, activities 10%.
- **Small samples:** an object with fewer than 30 eligible records carries a warning.
- **Critical floors,** independent of the composite:

  | Rule | Floor |
  |---|---|
  | Suppression conflicts | 100% pass |
  | Active ownership | ≥ 99% |
  | Unresolved duplicate accounts tied to open opportunities | 0 tolerated |

A 95 composite with a failing critical rule is a failing CRM.

## Every report shows

- evaluated, excluded, failed and unknown counts;
- rule-level and object-level results;
- the top contributors to lost points;
- the rule-set version and snapshot time.

An unevaluable rule is never scored as passing.

## Explaining movement

Break every change in the score into four parts:
- records that were fixed;
- new defects;
- population changes;
- rule changes.

When the rule set changes, recalculate the prior snapshot under the new rules and label it a rebaseline. Improvement that comes from excluding hard records is not progress.

Look for concentration by integration, form, import, owner, segment, record age and stage. A decline driven by one source needs a control on that source. A broad decline points at incentives or process.

**Worked example from the source:**
- **The composite rose** from 82 to 86 because contact completeness improved.
- **Opportunity health fell** from 91 to 78 because a new import created past-due close dates and ownerless deals.
- **Reporting "health improved four points"** would hide the regression that matters.

## Remediation queue

Rank rule-and-source combinations by severity × affected share × recurrence × downstream reach. Fix where defects are being created before paying down the backlog. Each item names:
- the source;
- the owner;
- the immediate containment;
- the durable control;
- the target metric;
- the review date.

## Cadence

Measure weekly for an operational CRM; review with leadership monthly. Annotate migrations, acquisitions, new integrations and rule changes on the trend line.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/ryan-iyengar/crm-health-scoring` (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._
