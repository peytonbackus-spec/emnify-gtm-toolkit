import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server  # noqa: E402
from shared_core.ai_governance import llm_client  # noqa: E402


@pytest.fixture(autouse=True)
def no_network_no_repo_writes(monkeypatch, tmp_path):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("GTM_LLM_MODE", raising=False)
    monkeypatch.setattr(llm_client, "OUTPUT_DIR", tmp_path)


def test_precision_audit():
    labels = [{"account_id": f"A{i}", "tool": "X", "correct": i < 8} for i in range(10)] + \
             [{"account_id": f"A{i}", "tool": "Y", "correct": i < 5} for i in range(10)]
    out = server.precision_audit(labels=labels, tool_a="X", tool_b="Y")
    x = next(t for t in out["per_tool"] if t["tool"] == "X")
    assert x["n"] == 10 and x["correct"] == 8 and x["precision"] == 0.8
    assert out["paired"]["a_only"] == 3 and out["paired"]["b_only"] == 0
    assert json.dumps(out)
    assert "error" in server.precision_audit(labels=[{"account_id": "1", "tool": "X", "correct": "maybe"}])
    assert "per_tool" in server.precision_audit(use_demo_data=True)


def test_capacity_model():
    out = server.capacity_model(pipeline_target_usd=6_000_000)
    assert out["opps_needed"] == 58 and out["sqls_needed"] == 104
    assert out["meetings_needed"] == 174
    assert "error" in server.capacity_model(inbound_share=1.5)
    assert "error" in server.capacity_model(avg_opp_size_usd=0)


def test_vp_brief_no_disk_write():
    out = server.vp_brief("snapshot")
    assert out["mode"] == "snapshot" and len(out["markdown"]) > 100
    assert len(server.vp_brief("full")["markdown"]) > len(out["markdown"])
    assert "error" in server.vp_brief("bogus")


def test_llm_mock_and_pii_guard():
    rec = {"account_name": "Acme", "ssn_field": "123-45-6789",
           "notes": "email jo@acme.com, ssn 123-45-6789, card 4111 1111 1111 1111, call 415-555-1234"}
    out = server.pii_guarded_llm_json(rec, "Summarise", ["account_name", "notes"])
    assert out["mode"] == "mock"
    blob = json.dumps(out)
    for leak in ("jo@acme.com", "123-45-6789", "4111 1111 1111 1111", "415-555-1234"):
        assert leak not in blob
    assert "ssn_field" not in out["sanitized_record"]  # non-allow-listed field dropped
    assert any("EMAIL" in a for a in out["pii_actions"])


def test_live_mode_without_key_returns_error(monkeypatch):
    monkeypatch.setenv("GTM_LLM_MODE", "anthropic")
    out = server.pii_guarded_llm_json({"account_name": "A"}, "t", ["k"])
    assert "ANTHROPIC_API_KEY" in out["error"]


def test_tools_registered():
    import asyncio
    names = {t.name for t in asyncio.run(server.mcp.list_tools())}
    assert names == {"precision_audit", "capacity_model", "vp_brief", "pii_guarded_llm_json"}
