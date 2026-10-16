import json
from pathlib import Path

import pytest

from integrations import clients, retry
from integrations.contract_check import CONTRACTS, check, load_contract

N8N = Path(__file__).resolve().parent.parent / "integrations" / "n8n"


def test_contracts_accept_and_reject():
    c = load_contract("salesforce_account_upsert")
    ok = {"domain": "a.example", "iot_vertical": "robotics", "provenance": {}, "approved_by": "u1"}
    ok["provenance"] = {"x": "zoominfo"}
    assert check(ok, c) == []
    bad = check({"domain": "nope", "iot_vertical": "submarines", "provenance": {"x": "y"}}, c)
    assert any("domain" in e for e in bad) and any("vertical" in e for e in bad) and any("approved_by" in e for e in bad)


def test_every_contract_has_idempotency_key():
    for p in CONTRACTS.glob("*.yaml"):
        assert "idempotency_key" in load_contract(p.stem), p.name


def test_n8n_workflows_are_wellformed():
    for p in N8N.glob("*.json"):
        wf = json.loads(p.read_text())
        names = {n["name"] for n in wf["nodes"]}
        assert len(names) == len(wf["nodes"])
        for src, conns in wf["connections"].items():
            assert src in names
            for branch in conns["main"]:
                for link in branch:
                    assert link["node"] in names
        assert wf["active"] is False


def test_retry_backoff_and_dead_letter():
    calls, sleeps = [], []

    def flaky():
        calls.append(1)
        raise ConnectionError("down")

    retry.DEAD_LETTER.clear()
    with pytest.raises(ConnectionError):
        retry.with_retry(flaky, attempts=3, base_delay=1, sleep=sleeps.append, context={"id": "A1"})
    assert len(calls) == 3 and sleeps == [1, 2] and retry.DEAD_LETTER[0]["id"] == "A1"


def test_non_transient_errors_fail_fast():
    n = []

    def bad():
        n.append(1)
        raise ValueError("contract")

    with pytest.raises(ValueError):
        retry.with_retry(bad, sleep=lambda s: None)
    assert len(n) == 1


def test_client_stubs_require_credentials(monkeypatch):
    for cls in (clients.AmplemarketClient, clients.AttentionClient, clients.WeflowClient, clients.ClayClient):
        for v in cls.env:
            monkeypatch.delenv(v, raising=False)
        with pytest.raises(RuntimeError):
            cls()
