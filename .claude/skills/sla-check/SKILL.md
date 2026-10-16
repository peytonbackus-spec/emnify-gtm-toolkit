---
name: sla-check
description: Use when the user asks whether MQL-to-SAL acceptance SLAs are being met, by SDR or lead source, or which accepted leads are stuck in Working too long.
---

# sla-check

Drives `gtm_engineer/lead_lifecycle/lifecycle_sla.py`. It reports MQL to SAL acceptance time against the SLA, split by SDR and by lead source, plus leads stuck in Working beyond the SAL to SQL window. The related lead-to-opportunity step is covered by `gtm_engineer/lead_routing/route_leads.py` and is not part of this skill.

## Inputs to ask for
- Which company config? Default `config/example.yaml`; override with `GTM_CONFIG=/path/to/file.yaml`. Targets live at `lead_lifecycle.sla_hours` (`mql_to_sal` in hours, `sal_to_sql_days`).
- Leads come from `sample_data/leads.csv`. There is no flag to change the data file.
- Does the user want a different SLA threshold? Change it in the config, not in code.

## Commands
```bash
python3 -m gtm_engineer.lead_lifecycle.lifecycle_sla
```
Run from the repo root. No CLI flags, read-only (writes no files).

## Output format
- Header with the SLA hours and overall % met.
- "By SDR" and "By lead source" tables: key, accepted, within_sla, sla_% (sorted worst first).
- Count of leads stuck in Working beyond `sal_to_sql_days`, and up to 10 of them with days_since_sal.
Report: overall %, worst SDR and worst source, and the stuck count.

## Failure modes
1. `FileNotFoundError` for `leads.csv` or `GTM_CONFIG`, or `KeyError: 'lead_lifecycle'`: the config lacks the `lead_lifecycle.sla_hours` block. Copy it from `config/example.yaml`.
2. Only leads with a non-empty `mql_to_sal_hours` count toward the %, and stuck leads need `status` Working plus a `sal_date`. Empty or mis-formatted columns silently shrink the totals, so check `accepted` counts against the lead count before drawing conclusions.
