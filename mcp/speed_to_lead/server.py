"""Speed-to-Lead SLA MCP server (FastMCP, stdio).

Tools: crm_read_new_leads, calendar_read_no_shows, evaluate_sla_breach,
slack_notify, sequencer_enqueue.  Backends are chosen by env
SPEED_TO_LEAD_ADAPTERS (e.g. "crm=json,notifier=mock"; default all mock).

Safety: slack_notify and sequencer_enqueue are DRY-RUN unless
ALLOW_LIVE_WRITES=1 AND the tool argument confirm=true.

Derived from speed_to_lead_server.py (speed-to-lead-sla). evaluate_sla_breach
logic is unchanged.

    python server.py            # MCP server over stdio
    python server.py --selftest # smoke test, no MCP client needed
"""
import argparse
import json
import os
import sys
from datetime import timedelta
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import adapters  # noqa: E402
from adapters import now_utc, parse_iso  # noqa: E402

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # shim so --selftest works without the mcp package
    class FastMCP:  # type: ignore
        def __init__(self, *_a, **_k): pass
        def tool(self, *_a, **_k):
            return lambda fn: fn
        def run(self):
            raise RuntimeError("The 'mcp' package is not installed; pip install -r requirements.txt")

mcp = FastMCP("speed-to-lead-sla")

# SLA windows by score tier, per wiki/skills/sales-development-strategy.md
SLA_MINUTES_BY_TIER = {
    "Tier 1 (Hot)": 5,
    "Tier 2 (Warm)": 30,
    "Tier 3 (Cold)": 1440,  # next business day
}


def live_writes_allowed(confirm: bool) -> bool:
    return os.environ.get("ALLOW_LIVE_WRITES") == "1" and confirm is True


def _dry_run_reason(confirm: bool) -> str:
    missing = []
    if os.environ.get("ALLOW_LIVE_WRITES") != "1":
        missing.append("env ALLOW_LIVE_WRITES=1")
    if confirm is not True:
        missing.append("tool arg confirm=true")
    return "dry run; to act, set " + " and ".join(missing)


@mcp.tool()
def crm_read_new_leads(since_minutes: int = 60) -> list:
    """Read leads created in the CRM within the last `since_minutes` minutes
    (backend chosen by SPEED_TO_LEAD_ADAPTERS crm=mock|json|hubspot)."""
    return adapters.get_adapter("crm").read_new_leads(since_minutes)


@mcp.tool()
def calendar_read_no_shows(lookback_hours: int = 24) -> list:
    """Read meetings within `lookback_hours` marked no-show with no recovery
    cadence yet triggered (calendar=mock|json|hubspot)."""
    return adapters.get_adapter("calendar").read_no_shows(lookback_hours)


@mcp.tool()
def evaluate_sla_breach(lead: dict) -> dict:
    """
    Given a lead record (as returned by crm_read_new_leads), determine
    its SLA tier, deadline, and whether it is currently breached or
    approaching breach (within 20% of its window).
    """
    tier = lead.get("score_tier", "Tier 3 (Cold)")
    window_minutes = SLA_MINUTES_BY_TIER.get(tier, SLA_MINUTES_BY_TIER["Tier 3 (Cold)"])
    created_at = parse_iso(lead["created_at"])
    deadline = created_at + timedelta(minutes=window_minutes)
    now = now_utc()
    minutes_remaining = (deadline - now).total_seconds() / 60

    if minutes_remaining < 0:
        status = "BREACHED"
    elif minutes_remaining <= window_minutes * 0.2:
        status = "AT_RISK"
    else:
        status = "OK"

    return {
        "lead_id": lead.get("id"),
        "tier": tier,
        "sla_window_minutes": window_minutes,
        "deadline_utc": deadline.isoformat(),
        "minutes_remaining": round(minutes_remaining, 1),
        "status": status,
    }


@mcp.tool()
def slack_notify(channel: str, message: str, confirm: bool = False) -> dict:
    """Post an SLA alert to a channel. DRY RUN by default: only sends when env
    ALLOW_LIVE_WRITES=1 AND confirm=true (notifier=mock|json|slack)."""
    if not live_writes_allowed(confirm):
        return {"ok": True, "dry_run": True, "would_send": {"channel": channel, "message": message},
                "reason": _dry_run_reason(confirm)}
    return {"dry_run": False, **adapters.get_adapter("notifier").notify(channel, message)}


@mcp.tool()
def sequencer_enqueue(contact_id: str, cadence_name: str, confirm: bool = False) -> dict:
    """Enqueue a contact into a named cadence. DRY RUN by default: only acts when
    env ALLOW_LIVE_WRITES=1 AND confirm=true (sequencer=mock|json|hubspot).
    Production use should pass the CASL consent gate first."""
    if not live_writes_allowed(confirm):
        return {"ok": True, "dry_run": True,
                "would_enqueue": {"contact_id": contact_id, "cadence_name": cadence_name},
                "reason": _dry_run_reason(confirm)}
    return {"dry_run": False, **adapters.get_adapter("sequencer").enqueue(contact_id, cadence_name)}


def _selftest() -> None:
    print("adapters:", adapters.parse_selection(), "| live writes:",
          os.environ.get("ALLOW_LIVE_WRITES") == "1")
    print("=== crm_read_new_leads ===")
    leads = crm_read_new_leads(since_minutes=10_000_000)
    print(json.dumps(leads, indent=2))
    print("\n=== evaluate_sla_breach (each lead) ===")
    for lead in leads:
        result = evaluate_sla_breach(lead)
        print(json.dumps(result, indent=2))
        if result["status"] in ("BREACHED", "AT_RISK"):
            print(json.dumps(slack_notify(
                "revops-alerts",
                f"Lead {result['lead_id']} is {result['status']} "
                f"({result['tier']}, {result['minutes_remaining']} min remaining)"), indent=2))
    print("\n=== calendar_read_no_shows ===")
    no_shows = calendar_read_no_shows(lookback_hours=10_000_000)
    print(json.dumps(no_shows, indent=2))
    for m in no_shows:
        print(json.dumps(sequencer_enqueue(m["contact_id"], "no-show-recovery-v1")))
    print("\nSelf-test complete (writes are dry-run unless ALLOW_LIVE_WRITES=1 and confirm=true).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        _selftest()
    else:
        mcp.run()
