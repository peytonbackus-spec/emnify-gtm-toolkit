"""Consolidated GTM toolkit MCP server (stdio). Wraps functions from the gtm-revops-toolkit repo.

Run:  PYTHONPATH=<repo root> python server.py   (server.py also adds the repo root to sys.path itself)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(os.environ.get("GTM_TOOLKIT_ROOT") or Path(__file__).resolve().parents[2])
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from mcp.server.fastmcp import FastMCP  # noqa: E402

from gtm_engineer.enrichment import precision_audit as pa  # noqa: E402
from gtm_engineer.sdr_capacity.capacity_model import capacity  # noqa: E402
from gtm_strategy_ops.sales_leadership import vp_brief as vb  # noqa: E402
from shared_core.ai_governance import llm_client  # noqa: E402
from shared_core.ai_governance.pii_guard import sanitize_record  # noqa: E402

mcp = FastMCP("gtm-toolkit")

MAX_LABEL_ROWS = 20000


@mcp.tool()
def precision_audit(labels: list[dict[str, Any]] | None = None, tool_a: str | None = None,
                    tool_b: str | None = None, use_demo_data: bool = False) -> dict:
    """Compare contact/enrichment vendor precision from human-labelled results (Wilson 95% intervals,
    plus an exact McNemar paired test when two tools are named).

    Use when: you labelled sampled enrichment output as correct/incorrect and need to know whether
    vendor A is really better than vendor B, or how precise one vendor is.
    Inputs: labels = list of {"account_id": str, "tool": str, "correct": true/false/"yes"/"no"/1/0};
    tool_a / tool_b = optional tool names for the paired comparison; use_demo_data=true uses seeded
    synthetic labels (ToolA/ToolB) instead of labels.
    Example: precision_audit(labels=[{"account_id":"A1","tool":"X","correct":true},
    {"account_id":"A1","tool":"Y","correct":false}], tool_a="X", tool_b="Y")
    Returns: {"per_tool":[{tool,n,correct,precision,lo,hi}], "paired":{paired_n,a_only,b_only,both,
    neither,precision_diff_a_minus_b,p_value}|null, "report": str} or {"error": str}.
    """
    try:
        if use_demo_data:
            rows = pa.demo_rows()
            tool_a, tool_b = tool_a or "ToolA", tool_b or "ToolB"
        else:
            if not labels:
                return {"error": "provide labels or set use_demo_data=true"}
            if len(labels) > MAX_LABEL_ROWS:
                return {"error": f"too many label rows (max {MAX_LABEL_ROWS})"}
            rows = [{"account_id": str(r["account_id"]).strip(), "tool": str(r["tool"]).strip(),
                     "correct": pa._parse_bool(r["correct"])} for r in labels]
        per_tool = [vars(t) for t in pa.summarize(rows)]
        paired = pa.paired_comparison(rows, tool_a, tool_b) if tool_a and tool_b else None
        return {"per_tool": per_tool, "paired": paired, "report": pa.format_report(rows, tool_a, tool_b)}
    except (KeyError, ValueError) as exc:
        return {"error": f"invalid input: {exc}"}


@mcp.tool()
def capacity_model(pipeline_target_usd: float = 6_000_000, avg_opp_size_usd: float = 105_000,
                   sql_to_opp_rate: float = 0.55, meeting_to_sql_rate: float = 0.60,
                   inbound_share: float = 0.45, sdr_meetings_per_month: float = 14,
                   ramp_months: int = 3, months: int = 3, connects_per_meeting: float = 9,
                   dials_per_connect: float = 14) -> dict:
    """Work backward from a sourced-pipeline target to SDR headcount and dial volume.

    Use when: sizing an SDR team, or testing how a conversion-rate change moves headcount.
    Inputs: pipeline_target_usd for the period; avg_opp_size_usd; funnel rates as fractions 0-1
    (sql_to_opp_rate, meeting_to_sql_rate, inbound_share); sdr_meetings_per_month per ramped rep;
    ramp_months; months in the period. Defaults are illustrative [ASSUME] values; replace with actuals.
    Example: capacity_model(pipeline_target_usd=6000000, meeting_to_sql_rate=0.5)
    Returns: {opps_needed, sqls_needed, meetings_needed, outbound_meetings, meetings_per_month,
    ramped_sdrs_needed, if_hiring_now_sdrs_needed, monthly_dials_outbound} or {"error": str}.
    """
    for name, v in (("avg_opp_size_usd", avg_opp_size_usd), ("sql_to_opp_rate", sql_to_opp_rate),
                    ("meeting_to_sql_rate", meeting_to_sql_rate), ("sdr_meetings_per_month", sdr_meetings_per_month)):
        if v <= 0:
            return {"error": f"{name} must be > 0"}
    if not 0 <= inbound_share <= 1:
        return {"error": "inbound_share must be between 0 and 1"}
    if months <= 0 or pipeline_target_usd < 0:
        return {"error": "months must be > 0 and pipeline_target_usd >= 0"}
    return capacity(pipeline_target_usd, avg_opp_size_usd, sql_to_opp_rate, meeting_to_sql_rate,
                    inbound_share, sdr_meetings_per_month, ramp_months, months,
                    connects_per_meeting, dials_per_connect)


@mcp.tool()
def vp_brief(mode: str = "snapshot") -> dict:
    """Generate the VP of Sales brief (Markdown) from the repo's configured data (sample_data/ and
    the active GTM_CONFIG; nothing is written to disk).

    Use when: you need the weekly leadership snapshot (one screen: number, risks, deals to act on,
    asks) or the full version with rep scorecard, segment table, stage velocity and deal board.
    Inputs: mode = "snapshot" (default) or "full".
    Example: vp_brief(mode="snapshot")
    Returns: {"mode": str, "markdown": str} or {"error": str}.
    """
    if mode not in ("snapshot", "full"):
        return {"error": "mode must be 'snapshot' or 'full'"}
    d = vb.gather()
    return {"mode": mode, "markdown": vb.snapshot(d) if mode == "snapshot" else vb.full(d)}


def _llm_mode() -> str:
    """mock unless a key is present and live mode was not explicitly disabled."""
    requested = os.getenv("GTM_LLM_MODE", "").lower()
    if requested == "mock":
        return "mock"
    if requested == "anthropic" or os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    return "mock"


@mcp.tool()
def pii_guarded_llm_json(record: dict[str, Any], task: str, required_keys: list[str],
                         system_prompt: str = "You are a precise GTM analyst. Use only the record provided.",
                         prompt_id: str = "mcp-adhoc@1") -> dict:
    """Ask an LLM for a JSON answer about a CRM record, with the repo's PII guard always in the path:
    fields not on the allow-list are dropped and emails, phones, SSNs, card/account numbers are
    redacted BEFORE the model sees the record. Every call is audit-logged by the repo's LLMClient.

    Use when: you want an AI summary/classification of an account or deal without leaking PII.
    Inputs: record = flat dict of CRM fields (e.g. account_name, segment, amount, stage, notes);
    task = instruction; required_keys = JSON keys the answer must contain.
    Model: GTM_LLM_MODEL, then ANTHROPIC_MODEL, then the client default. Mode is mock (deterministic,
    offline) unless ANTHROPIC_API_KEY is set; GTM_LLM_MODE=anthropic without a key returns an error.
    Example: pii_guarded_llm_json({"account_name":"Acme","notes":"call jo@acme.com"},
    "Summarise risk", ["summary"])
    Returns: {"mode", "result": {...required keys}, "sanitized_record": {...}, "pii_actions": [str]}
    or {"error": str}.
    """
    if not required_keys:
        return {"error": "required_keys must not be empty"}
    mode = _llm_mode()
    if mode == "anthropic" and not os.getenv("ANTHROPIC_API_KEY"):
        return {"error": "ANTHROPIC_API_KEY is not set; unset GTM_LLM_MODE or set it to 'mock' for offline mode"}
    clean, pii_actions = sanitize_record(record)

    def mock(c: dict) -> dict:
        return {k: c.get(k, f"[mock] {task[:80]}") for k in required_keys}

    try:
        client = llm_client.LLMClient(mode=mode)
        result = client.complete_json(prompt_id=prompt_id, system=system_prompt, record=record,
                                      required_keys=list(required_keys), mock_responder=mock, task=task)
    except ImportError:
        return {"error": "live mode needs the 'anthropic' package (pip install anthropic)"}
    except llm_client.OutputContractError as exc:
        return {"error": f"model output rejected: {exc}"}
    except Exception as exc:  # network/auth/etc: never crash the server
        return {"error": f"LLM call failed: {type(exc).__name__}: {exc}"}
    return {"mode": mode, "result": result, "sanitized_record": clean, "pii_actions": pii_actions}


if __name__ == "__main__":
    mcp.run()
