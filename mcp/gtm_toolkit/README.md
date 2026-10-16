# gtm-toolkit MCP server

Consolidated MCP server (stdio, FastMCP) that wraps existing functions in this repo. No logic is reimplemented.
No tool takes a file path: inputs are inline data, or the repo's `sample_data/` and active config.

| Tool | Wraps | Purpose |
|---|---|---|
| `precision_audit` | `gtm_engineer/enrichment/precision_audit.py` (`summarize`, `paired_comparison`, `format_report`, `demo_rows`) | Vendor precision with Wilson intervals + paired McNemar test from inline labels |
| `capacity_model` | `gtm_engineer/sdr_capacity/capacity_model.py` (`capacity`) | Pipeline target (USD) to SDR headcount and dials |
| `vp_brief` | `gtm_strategy_ops/sales_leadership/vp_brief.py` (`gather`, `snapshot`, `full`) | VP brief Markdown from sample data; never writes to `outputs/` |
| `pii_guarded_llm_json` | `shared_core/ai_governance/llm_client.py` (`LLMClient.complete_json`) + `pii_guard.sanitize_record` | LLM JSON answer with allow-list + PII redaction always applied, audit-logged |

Not included: ROI calculators. The canonical repo has none (only company-specific ones exist in sibling repos, which are deliberately not ported).

LLM behavior: mock mode (offline, deterministic) unless `ANTHROPIC_API_KEY` is set. `GTM_LLM_MODE=mock` forces mock; `GTM_LLM_MODE=anthropic` without a key returns an error dict. Model: `GTM_LLM_MODEL`, then `ANTHROPIC_MODEL`, then the client default.

## Setup (needs Python 3.10+; the `mcp` package does not support 3.9)

```
cd mcp/gtm_toolkit
uv venv --python 3.12 .venv && uv pip install -p .venv/bin/python -r requirements.txt
.venv/bin/python -m pytest -q
```

To reproduce the exact versions this server was last verified against, install with `pip install -r requirements.lock` instead.

## Register with Claude Code (print only; run it yourself)

```
claude mcp add gtm-toolkit -e PYTHONPATH=$HOME/gtm-revops-toolkit -- $HOME/gtm-revops-toolkit/mcp/gtm_toolkit/.venv/bin/python $HOME/gtm-revops-toolkit/mcp/gtm_toolkit/server.py
```

Add `-e ANTHROPIC_API_KEY=...` for live mode. `server.py` also inserts the repo root (or `GTM_TOOLKIT_ROOT`) into `sys.path`.
