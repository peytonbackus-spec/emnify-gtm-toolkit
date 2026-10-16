# Repo map

Audit date: 2026-10-08. `~/gtm-revops-toolkit` is the canonical toolkit.

**Why canonical:** newest history (last commit 2026-10-07), config-driven template with no hardcoded company values, the broadest module layout (`gtm_engineer/`, `gtm_strategy_ops/`, `shared_core/`) and a tested `make new COMPANY=...` flow. `~/dev/gtm-revops-toolkit` is older (2026-09-28), has a different layout (`gtm-os/`, `wiki/`) and is richer only in prompt/agent docs and wiki content, so it is mined for files rather than promoted.

| repo | role | last commit | files worth porting (names only) |
|---|---|---|---|
| ~/gtm-revops-toolkit | canonical | 2026-10-07 | n/a |
| ~/dev/gtm-revops-toolkit | archive (source of ports) | 2026-09-28 | gtm-os/agents/* (67 prompt files), gtm-os/code/scoring/churn_prediction_pipeline.py, gtm-os/code/scoring/meddpicc_health_engine.py, gtm-os/code/sfdc_pql_ingestor.py, gtm-os/code/revops_tech_debt_tracker.py, core/engine/l2a_matcher.py, core/engine/rules_engine.py, scripts/outbound_engine.py, gtm-os/mcp/speed-to-lead/speed_to_lead_server.py. Already ported to canonical: gtm-os/contracts/*, gtm-os/schemas/*, modules/gtm_engineering/*.md (now under docs/) |
| company-specific toolkit A | company-specific | 2026-10-07 | none; derived from canonical, 54 files diverge |
| company-specific toolkit B | company-specific | 2026-10-07 | none; derived from canonical, 73 files diverge |
| company-specific toolkit C | company-specific; older lineage | 2026-09-02 | none; same structure as legacy/dev, scripts/gtm_reporting_agent.py only differs by model env var |
| company-specific toolkit D | company-specific | 2026-09-14 | ROI calculator script and menu script |
| ~/_legacy-gtm-2nd-brain-2026-08 | legacy | 2026-08-31 | none; build_gtm_system.py, scripts/sync_vault.sh only if the vault sync is revived |

Code files listed as "worth porting" were not copied: they depend on `core/models` or on dev's layout and need adapting to canonical's modules first.

Third-party skills: 18 skills from swan-gtm/gtm-skills (MIT) were ported on 2026-10-13 as contracts, playbooks and governance notes. See [docs/crosswalks/swan-gtm-skills.md](crosswalks/swan-gtm-skills.md).

## ~/workflows

| file | purpose |
|---|---|
| README.md | Index of the Clay, n8n, HubSpot and Claude Code workflow notes. |
| clay_webhook_listener.py | FastAPI webhook that receives leads from Clay and matches them to accounts (lead-to-account matcher). |
| claude-code/report-generator.md | Claude Code workflow for generating the recurring GTM report. |
| claude-code/sequence-monitor.md | Claude Code workflow for monitoring outbound sequence health. |
| clay/prospect-enrichment.md | Clay table design for prospect enrichment. |
| clay/signal-monitor.md | Clay setup for watching buying signals. |
| hubspot/properties.md | HubSpot custom property definitions used by the workflows. |
| n8n/crm-health-automation.md | n8n flow for recurring CRM data-health checks. |
| n8n/weekly-report-automation.md | n8n flow that assembles and sends the weekly report. |
