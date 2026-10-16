---
type: area
category: revops
tags:
  - area
  - hubspot
  - lifecycle
  - workflows
status: active
last_updated: 2026-10-13
---

# HubSpot Lifecycle and Workflow Recipes

Module: `docs/specs/architecture`. Expands the [HubSpot spec stub](../specs/architecture/HubSpot.md). Scoring follows the toolkit's two-axis model (decision #3) and the [Lead Scoring / PQL spec](../specs/lead-management/Lead_Scoring_PQL_Spec.md); this playbook covers the HubSpot configuration around it.

## Executive Summary

Design for reporting first: if you can't name the report or automation a property feeds, don't create it. Automate objective transitions and leave the human qualification gate manual. Every workflow that emails, merges, creates companies or reassigns owners carries an explicit approval or suppression check (decision #6, [`hitl.py`](../../shared_core/ai_governance/hitl.py)).

## Three separate tracking mechanisms

| Field | Whose view | Answers |
|---|---|---|
| Lifecycle stage | Marketing | Where the contact is in the revenue journey |
| Deal stage | Sales | Where the opportunity is in the sales process |
| Lead status | SDR | What follow-up is happening |

Don't make one field do another's job.

## Lifecycle rules

- **Stages:** Subscriber, Lead, MQL, SQL, Opportunity, Customer, Evangelist. Add a custom stage only when a report needs it.
- **Movement:** forward is the default. Backward moves are deliberate (win-back, data correction) and logged. More than 5% of contacts in "Other" means the definitions are broken.
- **Automate the objective moves:** score crosses the MQL threshold, a deal is created, a deal is won.
- **Keep MQL to SQL manual:** a rep accepting the lead is the most important quality gate.
- **Date-stamp every transition** (`rev_mql_date`, `rev_sql_date` and so on) so velocity is reportable.
- **Check the shape:** the stage distribution should look like a funnel. If it doesn't, the definitions are wrong.

## Pipelines

- One pipeline per motion: new business and expansion are separate.
- Require close date, amount and owner on every deal, and a dropdown loss reason on Closed Lost. HubSpot ignores required fields on the first stage at creation, so use a task within 24 hours instead.
- Replace default stage probabilities with 12-month historical rates.
- HubSpot can't trigger on time-in-stage, so stamp `rev_last_stage_change_date` on every change and use it to drive stale-deal tasks. Policy is in [Pipeline Visibility](Pipeline_Visibility_and_Hygiene.md).

## Property standards

- **Prefixes:** `rev_`, `mktg_`, `sales_`, `cs_`, `int_` (integration-synced), `calc_` (calculated).
- **Types:** snake_case, currency in the name (`_eur`), picklists rather than free text for anything categorical.
- **Fields to start with:**
  - contact: `rev_icp_fit`, `rev_lead_source` (set once, never overwritten), `rev_first_touch_date`;
  - deal: `rev_deal_source`, `rev_competitor`, `rev_closed_lost_reason`, `rev_expansion_type`;
  - company: `rev_icp_tier`, `rev_customer_since`, `rev_arr`, `rev_health_score`.
- **Governance:** create and deprecate under [field and agent-write governance](../../shared_core/data_quality/field-and-agent-write-governance.md).

## Workflow recipes, re-gated

| Recipe | Trigger | Actions | Gate we added |
|---|---|---|---|
| Auto-MQL | Fit and engagement thresholds both met | Set MQL, stamp the date, task the owner to accept or reject within 24h | Suppression and consent check before any email enrollment |
| Accept to SQL | Rep sets lead status to Working | Set SQL, stamp the date | Human action is the trigger |
| Deal won | Stage = Closed Won | Customer lifecycle, `rev_customer_since`, CS onboarding task | None needed (internal only) |
| Stale deal | `rev_last_stage_change_date` older than X and the deal is open | Owner task; escalate high-value deals to the manager | **Never** auto-close as "No Decision"; the manager decides |
| Possible duplicate | New contact matches on email, or name plus company | Review task with a link to the existing record | **Never auto-merge**; merges go through the [CRM cleanup contract](../contracts/crm-cleanup-contract.md) |
| Missing firmographics | Contact created without company data | Enrich, then a review task | **No implicit company creation**; resolve before create; fill-if-empty only |
| Industry standardization | Industry value not on the standard list | Map to the standard value, note the original | Change logged; reversible |
| Re-engagement | MQL/SQL inactive 30+ days | Task first; any nurture email only for contacts with marketing consent | CASL/consent gate; unsubscribed contacts excluded |
| GDPR Art. 21 / do-not-contact | Objection or unsubscribe | Unenroll from **all** workflows and sequences, flag and date-stamp, never re-enroll without new consent | Mandatory, runs before everything else |
| Renewal | 60/45/30 days before contract end | CSM and AE tasks, escalate if no quote | Native Contracts object if Commerce Hub is available |

## Scoring fairness

Keep the fit score to firmographic criteria. Audit any title-seniority or location weight that could stand in for a protected characteristic.

## Not carried over

- **Breeze agent pricing and feature dates:** unverified vendor claims, which go to the GTM 2nd Brain register.
- **The source's two conflicting MQL thresholds:** thresholds come from back-testing per the scoring spec.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/rutger-katz/revops-hubspot` (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._
