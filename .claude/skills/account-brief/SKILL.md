---
name: account-brief
description: Use when the user wants AI account research or qualification briefs for new/MQL/enriching leads, with a human-review queue of recommended next actions.
---

# account-brief

Drives `gtm_engineer/ai_research/account_research.py`. It scores leads, takes the first 12 with status New, MQL or Enriching, builds a brief per lead, applies the HITL policy and writes a review queue. Offline mock mode is the default and needs no API key.

## Inputs to ask for
- Mock or live? Default is mock. Live needs `GTM_LLM_MODE=anthropic`, `ANTHROPIC_API_KEY`, the `anthropic` package (`pip install -e .[live]`), and optionally `GTM_LLM_MODEL` (falls back to `ANTHROPIC_MODEL`, then the default).
- Which company config? Default is `config/example.yaml`. Override with `GTM_CONFIG=/path/to/file.yaml`.
- Data comes from `sample_data/accounts.csv` and `sample_data/leads.csv`. There is no flag to change the data directory.

## Commands
```bash
python3 -m gtm_engineer.ai_research.account_research                      # mock mode
GTM_LLM_MODE=anthropic python3 -m gtm_engineer.ai_research.account_research   # live mode
```
Run from the repo root. The module has no CLI flags.

## Output format
- Table on stdout: lead_id, company, grade, products, next_action, confidence, decision (`auto_apply` or `human_review`).
- `outputs/review_queue_account_research.csv`: the same rows plus use_case, unknowns, review_status, reviewer, reviewer_action.
- `outputs/ai_audit_log.jsonl`: one line appended per call (prompt id, mode, PII audit).
Report: count of `auto_apply` vs `human_review`, and the human_review leads by company and next_action.

## Failure modes
1. `FileNotFoundError` for a CSV or for `GTM_CONFIG`: the path is wrong or `sample_data/` was not generated. Run `make data` (see Makefile `data` target) or fix the path.
2. Live mode: `ModuleNotFoundError: anthropic` or an auth error means the optional dependency or `ANTHROPIC_API_KEY` is missing. Fall back to mock mode and say so. A missing model env var only logs a warning and uses the default.
