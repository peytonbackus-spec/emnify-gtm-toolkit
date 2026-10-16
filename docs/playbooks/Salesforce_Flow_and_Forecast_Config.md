---
type: area
category: revops
tags:
  - area
  - salesforce
  - flow
  - forecasting
status: active
last_updated: 2026-10-13
---

# Salesforce Flow and Forecast Configuration

Modules: `shared_core/data_model` ([object model](../../shared_core/data_model/salesforce-object-model.md)) and `docs/specs/salesforce` ([MEDDPICC validation spec](../specs/salesforce/SFDC_MEDDPICC_Validation_Spec.md)). Related: [forecast tool configuration](../../gtm_strategy_ops/forecast_tool_admin/forecast-tool-configuration-spec.md) and the [routing flow spec](../../gtm_engineer/lead_routing/salesforce-routing-flow-spec.md).

## Executive Summary

- One entry point per object, Flow first.
- Validation layered from field to record to Flow.
- Forecast snapshots, so accuracy can be measured at all.

## Automation architecture

- **At most three record-triggered Flows per object:**
  - before-save: defaults, validation, same-record updates;
  - after-save: other records, notifications, integrations, async paths for callouts;
  - before-delete.

  Branch inside each Flow with Decision elements.
- **Naming:** `Object_Trigger_Purpose_vN` (for example `Opportunity_BeforeSave_StageValidation_v1`), with a dated description of each version.
- **Feature flags** in Custom Metadata Types, so logic switches without a redeploy. No hardcoded record, user or queue IDs.
- **Flow vs Apex:** Flow by default. Use Apex invocable actions for batches above about 10K records, very complex logic, retries and error handling, or sub-second callouts.
- **Never mix Apex triggers and Flows** on the same object.
- **Every Flow has a fault path** that notifies an admin.
- **No DML inside loops.**
- **Guard against recursion:** prefer before-save for same-record updates.
- **Migrating from Process Builder and Workflow Rules:**
  1. Audit what runs per object.
  2. Map the firing order.
  3. Consolidate into one after-save Flow.
  4. Test in a sandbox, because execution order changes.
  5. Migrate one object at a time.
  6. Deactivate the old automation; don't delete it.

## Opportunity stage gates

Stages and exit criteria live in [stage-definitions.md](../../gtm_strategy_ops/opportunity_lifecycle/stage-definitions.md). Enforce them with validation:

| Rule | Logic |
|---|---|
| No stage skipping | Advance one stage at a time; Closed Lost allowed from any stage |
| Amount at Proposal | Stage ≥ Proposal requires an amount |
| Contact role | Stage ≥ Qualification requires at least one OpportunityContactRole |
| Loss reason | Closed Lost requires a loss reason (and a competitor if the loss was competitive) |
| Next step | Open stages require a next step with a future date |

Use record types when the process differs but the data model is the same (new business, renewal, expansion). Use custom objects when the data model itself differs.

## Forecast configuration

- **Categories:** Pipeline, Best Case, Commit, Closed, Omitted. A deal sitting in Commit for more than 30 days without moving is not a Commit; downgrade it.
- **Forecast type:** opportunity amount by default. Use product, split or product family only when the business needs it. Use revenue splits (totalling 100%) for quota credit, and overlay splits for influence.
- **`Forecast_Snapshot__c`:** period, snapshot date, rep, commit, best case, pipeline, actual and an accuracy formula, populated by a scheduled Flow at each forecast call. It feeds [`forecast_accuracy.py`](../../gtm_strategy_ops/forecasting/forecast_accuracy.py).
- **No formula fields as forecast-tool inputs.** Stamp the values with a Flow instead (decision #11).

## Duplicate management

Up to 5 active matching rules per object:
- Lead: email domain plus company, fuzzy.
- Contact: exact email, or name plus account.
- Account: exact website domain, or fuzzy name.

Duplicate rules alert by default, and block only on hard duplicates (exact contact email).

## Hygiene Flows

A scheduled scrub flags stale, stalled and zero-amount deals and creates owner tasks. **It does not move close dates.** An overdue close date becomes a task, per [Pipeline Visibility](Pipeline_Visibility_and_Hygiene.md).

## Not carried over

Agentforce, Data 360 and Einstein feature and date claims are unverified vendor statements, which go to the GTM 2nd Brain register. The source's reference-file links pointed at files that don't exist.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/rutger-katz/revops-salesforce` (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._
