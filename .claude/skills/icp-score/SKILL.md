---
name: icp-score
description: Use when the user wants leads graded for ICP fit and buying intent (grade like A1 to D4) with a recommended route for each, or wants the grade distribution.
---

# icp-score

Drives `gtm_engineer/lead_scoring/score_leads.py` (two-axis scoring: Fit letter A-D x Intent number 1-4). Weights, segments and personas come from the company config. Tuning the weights is a separate module, `gtm_engineer/lead_scoring/calibrate_scoring.py`.

## Inputs to ask for
- Which company config? Default `config/example.yaml`; override with `GTM_CONFIG=/path/to/file.yaml`. ICP definition lives under `lead_scoring`, `segments` and `personas` in that file.
- Leads come from `sample_data/leads.csv`. There is no flag to point at another file; to score other data, replace that CSV or use a config-driven copy of the repo (`make new COMPANY="..."`).
- Does the user want the distribution only, or also the top leads and the full CSV?

## Commands
```bash
python3 -m gtm_engineer.lead_scoring.score_leads
```
Run from the repo root. No CLI flags.

## Output format
- Grade distribution grid (Fit letter rows x Intent number columns).
- Recommendation counts (e.g. "MQL -> route to SDR now", "Nurture").
- Top 5 leads table: lead_id, company, title, segment, fit_score, intent_score, grade, recommendation.
- Full results in `outputs/scored_leads.csv` (tracked in git, so a rerun may change it).
Report: A1-B2 count, top recommendation buckets, and any odd distribution (for example almost everything in one cell).

## Failure modes
1. `FileNotFoundError` for `leads.csv` or `GTM_CONFIG`, or a `KeyError` on a config key: the config is missing the `lead_scoring`/`segments`/`personas` sections. Start from `config/example.yaml`.
2. Skewed grades (nearly all D4) usually mean signal dates that are old relative to `fiscal.as_of_date` in the config (decay is measured from that date; it defaults to today when unset), not bad weights. Check dates before recalibrating.
