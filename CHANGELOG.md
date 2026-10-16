# Changelog

## 0.5.0 (unreleased)
- New `gtm_strategy_ops/sales_leadership/`: VP of Sales brief (snapshot or full), rep scorecard, industry win/loss with 80% confidence ranges, stage velocity with drivers and fixes, deal board (Past due / Slipping / At risk / Stalled / Hot / On track), sales all-hands inputs (`--days 1` for "today"), VP intake questions, SQL.
- New `gtm_strategy_ops/sales_planning/`: AE capacity and hiring plan, quota vs capacity and next year's proposal, territory carve and balance, pipeline distribution with region-aware routing priority, CRM request intake process and triage (SLA, duplicates, priority inversions).
- New `gtm_engineer/marketing_ops/`: Marketing Ops RACI and joint cadence, campaign operations spec, channel funnel and ROI, W-shaped attribution, campaign and consent hygiene (M01–M09), demand plan by channel.
- Sample data: `opportunity_field_history.csv` (StageName and CloseDate changes), campaigns, campaign members, lead consent, CRM requests. Each uses its own seeded RNG, so existing files are unchanged.
- Semantic layer: `v_stage_history`, `v_close_date_pushes`. Config: `sales_team`, `sales_planning`, `sales_leadership`, `marketing_ops`, prior-quarter quota; new variable `[MARKETING_AUTOMATION]`.
- Scaffold: every fiscal-quarter label in the config (quota, bookings plan, current quarter) is relabelled for the chosen fiscal calendar, not only the current quarter; new scaffold test runs the new reports on a calendar-year repo.
- Fix: open opportunities could show a stage entry date before the opportunity existed; now clamped to the created date.
- AI Workflow Standard: the HITL part now says to fail closed when a hook or check fails; the Stop rule carries a notification owner and time limit; added an allow-rule re-test step after any agent-tool upgrade and four audit questions (reachable MCP servers and who added them, stop on check failure, spend cap with a named owner, who can join without an invite). Decision log: entry 24.

## 0.4.3 (unreleased)
- Added `gtm_engineer/enrichment/precision_audit.py` (Wilson intervals, exact paired comparison, blind labeling sheet, `--demo`) with tests, plus the Vendor Benchmark Verification playbook.
- AI governance standard: added plugin / mod admission questions and a sub-agent effort rule.
- Decision log: entries 17 and 18.

## 0.4.2
- SQL: current fiscal quarter and as-of date now come from config ({{CURRENT_FISCAL_QUARTER}}, {{AS_OF}}) instead of being hardcoded.
- Scaffold: generated repos no longer carry the scaffold test (it failed once the scaffolder removed itself) or the template-only how-to page.
- CI: pinned ruff to an explicit rule set (newer ruff defaults had turned on 100+ style rules); fixed the real findings, including an undefined-name bug in a prototype prompt.
- Sample data: forecast quarters are now labelled from the configured fiscal calendar, so calendar-year companies get correct labels.

## 0.4.1
- README rewritten: role colour system, lifecycle and template diagrams, config map, AI governance summary.

## 0.4.0 (template restructure)
- Single config (`config/example.yaml`) drives scoring, routing, SQL fiscal calendar, prompts and sample data.
- Shared core plus two role tracks (GTM Engineer, Strategy & Ops); earlier engines folded in or moved to `prototypes/`.
- `scripts/new_company.py` / `make new` scaffold a company repo.
- Private material moved out to a separate private vault; history-purge script provided.
