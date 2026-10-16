# Clay table spec: emnify account and contact enrichment

Spec only. No Clay workspace was opened or run to produce this (no live runs in this build). Every provider order,
threshold and cost below is a hypothesis: validate. The offline engine in [waterfall.py](waterfall.py) implements the
same logic so the rules can be tested before any credits are spent.

## Why a table spec at all

The posting makes Clay a must-have and says candidates will be asked to walk through a flow. This is the flow, written so it can be rebuilt in Clay in an afternoon and so each column has a stated reason.

## Flow: new account to Salesforce-ready record

| # | Column | Type | Source | Runs when | Why |
|---|---|---|---|---|---|
| 1 | `domain` | input | Salesforce export or list upload | always | Join key. Normalized (lowercase, no scheme, no `www`) before anything else |
| 2 | `dupe_key` | formula | `domain` | always | Stops a second row for an existing account. Same rule as [dedupe.py](dedupe.py) |
| 3 | `in_salesforce` | lookup | Salesforce Account by `Website_Domain__c` | `dupe_key` not seen | Skip enrichment for accounts that already have a CRM owner |
| 4 | `company_description` | enrichment | Clay native, then website scrape | not `in_salesforce` | Cheapest source of the vertical signal |
| 5 | `iot_vertical` | formula or Claude | keywords, then Claude on the description | description present | Fit gate. No vertical, no paid contact credits |
| 6 | `employee_count`, `industry`, `hq_country` | waterfall | ZoomInfo, Clay native, first party | vertical present | Provider order in [waterfall_rules.yaml](waterfall_rules.yaml) |
| 7 | `fit_score` | formula | outbound scoring rules | all of the above | Same weights as [outbound/scoring.py](../outbound/scoring.py) |
| 8 | `decision_maker_email` | waterfall | ZoomInfo, then Amplemarket lookup | `fit_score` above threshold | Contact credits only for accounts that pass |
| 9 | `ready_for_sfdc` | formula | required fields present and valid | always | Mirrors [field_mapping.yaml](field_mapping.yaml) |
| 10 | `push_to_salesforce` | HTTP / n8n webhook | n8n workflow | `ready_for_sfdc` and approved | Writes go through the review gate, see [integrations](../integrations/README.md) |

## Guardrails

- Credit cap per run: `guardrails.max_enrichment_credits_per_run` in [company.yaml](../company.yaml).
- Paid contact lookups only after the fit gate (columns 5 and 7).
- Nothing writes to Salesforce without a human approval on the first N runs, then an exceptions-only review. See [knowledge/process/enrichment-run.yaml](../knowledge/process/enrichment-run.yaml).
- Provider confidence below `min_confidence` is treated as a miss and the next provider runs.

## What to measure once it runs (hypothesis: validate)

- Fill rate per field per provider, and credits per filled field.
- Wrong-vertical rate on a hand-labelled sample (use the Wilson-interval audit in [gtm_engineer/enrichment/precision_audit.py](../gtm_engineer/enrichment/precision_audit.py)).
- Duplicate rate before and after.
