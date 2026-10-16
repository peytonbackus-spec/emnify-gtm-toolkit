"""Contract tests for all 5 tools on mock + json adapters, plus the write gate."""
import asyncio
import json

import pytest

import server

BACKENDS = ["", "crm=json,calendar=json,notifier=json,sequencer=json"]


@pytest.fixture(params=BACKENDS, ids=["mock", "json"])
def backend(request, monkeypatch):
    monkeypatch.setenv("SPEED_TO_LEAD_ADAPTERS", request.param)
    return request.param


def test_crm_read_new_leads(backend):
    leads = server.crm_read_new_leads(since_minutes=10_000)
    assert leads
    for l in leads:
        assert {"id", "score_tier", "created_at"} <= l.keys()
    assert server.crm_read_new_leads(since_minutes=0) == []


def test_calendar_read_no_shows(backend):
    ms = server.calendar_read_no_shows(lookback_hours=48)
    assert ms
    assert all(m["status"] == "no_show" and not m["recovery_triggered"] and m["contact_id"] for m in ms)


def test_evaluate_sla_breach_contract(backend):
    for l in server.crm_read_new_leads(since_minutes=10_000):
        r = server.evaluate_sla_breach(l)
        assert set(r) == {"lead_id", "tier", "sla_window_minutes", "deadline_utc",
                          "minutes_remaining", "status"}
        assert r["status"] in {"OK", "AT_RISK", "BREACHED"}


def test_evaluate_sla_logic_unchanged():
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    def lead(tier, mins):
        return {"id": "x", "score_tier": tier, "created_at": (now - timedelta(minutes=mins)).isoformat()}
    assert server.evaluate_sla_breach(lead("Tier 1 (Hot)", 1))["status"] == "OK"
    assert server.evaluate_sla_breach(lead("Tier 1 (Hot)", 4.5))["status"] == "AT_RISK"
    assert server.evaluate_sla_breach(lead("Tier 1 (Hot)", 6))["status"] == "BREACHED"
    assert server.evaluate_sla_breach(lead("Tier 2 (Warm)", 31))["sla_window_minutes"] == 30
    assert server.evaluate_sla_breach(lead("bogus", 10))["sla_window_minutes"] == 1440


def test_notify_dry_run_by_default(backend, env):
    r = server.slack_notify("revops", "hi")
    assert r["dry_run"] is True and r["would_send"] == {"channel": "revops", "message": "hi"}
    assert not list(env.glob("*.jsonl"))


def test_gate_requires_both(backend, env, monkeypatch):
    assert server.slack_notify("c", "m", confirm=True)["dry_run"] is True       # env missing
    monkeypatch.setenv("ALLOW_LIVE_WRITES", "1")
    assert server.slack_notify("c", "m")["dry_run"] is True                     # confirm missing
    assert server.sequencer_enqueue("c1", "cad")["dry_run"] is True
    monkeypatch.setenv("ALLOW_LIVE_WRITES", "true")                             # only "1" counts
    assert server.slack_notify("c", "m", confirm=True)["dry_run"] is True
    assert not list(env.glob("*.jsonl"))


def test_notify_and_enqueue_live(backend, env, monkeypatch):
    monkeypatch.setenv("ALLOW_LIVE_WRITES", "1")
    n = server.slack_notify("revops", "hi", confirm=True)
    s = server.sequencer_enqueue("003_x", "no-show-recovery-v1", confirm=True)
    assert n["ok"] and n["dry_run"] is False and s["ok"] and s["dry_run"] is False
    log = env / ("outbox.jsonl" if "json" in backend else "notification_log.jsonl")
    assert len(log.read_text().splitlines()) == 2


def test_mixed_selection(monkeypatch):
    monkeypatch.setenv("SPEED_TO_LEAD_ADAPTERS", "crm=json,notifier=mock")
    ids = {l["id"] for l in server.crm_read_new_leads(10_000)}
    assert "L-1001" in ids


def test_bad_selection(monkeypatch):
    monkeypatch.setenv("SPEED_TO_LEAD_ADAPTERS", "crm=salesforce")
    with pytest.raises(ValueError):
        server.crm_read_new_leads()
    monkeypatch.setenv("SPEED_TO_LEAD_ADAPTERS", "bogus=mock")
    with pytest.raises(ValueError):
        server.crm_read_new_leads()


def test_tools_registered_with_fastmcp():
    names = {t.name for t in asyncio.run(server.mcp.list_tools())}
    assert names == {"crm_read_new_leads", "calendar_read_no_shows", "evaluate_sla_breach",
                     "slack_notify", "sequencer_enqueue"}
    res = asyncio.run(server.mcp.call_tool("slack_notify", {"channel": "c", "message": "m"}))
    assert "dry_run" in json.dumps(res, default=str)
