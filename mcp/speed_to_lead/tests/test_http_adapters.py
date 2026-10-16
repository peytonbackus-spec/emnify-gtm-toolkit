"""HubSpot + Slack adapters against recorded fixtures with mocked HTTP (no network)."""
import json

import httpx
import pytest

import adapters
import server
from conftest import fixture


def client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_hubspot_crm_maps_contacts():
    seen = {}
    def h(req):
        seen["url"], seen["auth"], seen["body"] = str(req.url), req.headers["authorization"], json.loads(req.content)
        return httpx.Response(200, json=fixture("hubspot_contacts_search.json"))
    leads = adapters.HubSpotCRM(token="t", client=client(h)).read_new_leads(60)
    assert seen["url"] == "https://api.hubapi.com/crm/v3/objects/contacts/search"
    assert seen["auth"] == "Bearer t"
    assert seen["body"]["filterGroups"][0]["filters"][0]["propertyName"] == "createdate"
    assert leads[0] == {"id": "101", "name": "Ana Silva", "email": "ana@acme.example",
                        "company": "Acme", "score_tier": "Tier 1 (Hot)",
                        "created_at": "2026-10-08T12:00:00.000Z"}
    assert leads[1]["name"] == "Ben" and leads[1]["score_tier"] == "Tier 3 (Cold)"
    # output feeds evaluate_sla_breach unchanged
    assert server.evaluate_sla_breach(leads[0])["status"] in {"OK", "AT_RISK", "BREACHED"}


def test_hubspot_requires_token():
    with pytest.raises(adapters.AdapterError):
        adapters.HubSpotCRM(client=client(lambda r: httpx.Response(200, json={}))).read_new_leads(5)


def test_hubspot_http_error():
    c = client(lambda r: httpx.Response(401, json={"message": "bad token"}))
    with pytest.raises(adapters.AdapterError, match="401"):
        adapters.HubSpotCRM(token="t", client=c).read_new_leads(5)


def test_hubspot_calendar_no_shows():
    def h(req):
        if req.url.path.endswith("/meetings/search"):
            return httpx.Response(200, json=fixture("hubspot_meetings_search.json"))
        assert req.url.path == "/crm/v4/objects/meetings/9001/associations/contacts"
        return httpx.Response(200, json=fixture("hubspot_meeting_assoc.json"))
    ms = adapters.HubSpotCalendar(token="t", client=client(h)).read_no_shows(24)
    assert ms == [{"id": "9001", "contact_id": "101", "title": "Demo - Acme",
                   "scheduled_at": "2026-10-08T10:00:00.000Z", "status": "no_show",
                   "recovery_triggered": False}]


def test_hubspot_sequencer(monkeypatch):
    monkeypatch.setenv("HUBSPOT_SEQUENCE_USER_ID", "55")
    monkeypatch.setenv("HUBSPOT_SENDER_EMAIL", "rep@example.com")
    posted = {}
    def h(req):
        if req.method == "GET":
            return httpx.Response(200, json=fixture("hubspot_sequences.json"))
        posted["body"], posted["q"] = json.loads(req.content), dict(req.url.params)
        return httpx.Response(200, json=fixture("hubspot_enrollment.json"))
    r = adapters.HubSpotSequencer(token="t", client=client(h)).enqueue("101", "no-show-recovery-v1")
    assert posted["body"] == {"sequenceId": "seq-77", "contactId": "101", "senderEmail": "rep@example.com"}
    assert posted["q"] == {"userId": "55"}
    assert r["ok"] and r["enrollment"]["id"] == "enr-1"


def test_hubspot_sequencer_unknown_cadence(monkeypatch):
    monkeypatch.setenv("HUBSPOT_SEQUENCE_USER_ID", "55")
    monkeypatch.setenv("HUBSPOT_SENDER_EMAIL", "rep@example.com")
    c = client(lambda r: httpx.Response(200, json=fixture("hubspot_sequences.json")))
    with pytest.raises(adapters.AdapterError, match="nope"):
        adapters.HubSpotSequencer(token="t", client=c).enqueue("1", "nope")


def test_slack_notify_ok():
    seen = {}
    def h(req):
        seen["url"], seen["auth"], seen["body"] = str(req.url), req.headers["authorization"], json.loads(req.content)
        return httpx.Response(200, json=fixture("slack_ok.json"))
    r = adapters.SlackNotifier(token="xoxb-test", client=client(h)).notify("#revops", "hello")
    assert seen["url"] == "https://slack.com/api/chat.postMessage"
    assert seen["auth"] == "Bearer xoxb-test"
    assert seen["body"] == {"channel": "#revops", "text": "hello"}
    assert r["ok"] and r["ts"] == "1759924800.000100"


def test_slack_ok_false_raises():
    c = client(lambda r: httpx.Response(200, json=fixture("slack_err.json")))
    with pytest.raises(adapters.AdapterError, match="channel_not_found"):
        adapters.SlackNotifier(token="x", client=c).notify("#x", "m")


def test_slack_requires_token():
    with pytest.raises(adapters.AdapterError):
        adapters.SlackNotifier(client=client(lambda r: httpx.Response(200))).notify("#x", "m")


def test_dry_run_never_touches_network(monkeypatch):
    """With hubspot/slack selected, dry-run must not construct adapters or call HTTP."""
    monkeypatch.setenv("SPEED_TO_LEAD_ADAPTERS", "notifier=slack,sequencer=hubspot")
    def boom(*a, **k):
        raise AssertionError("network used")
    monkeypatch.setattr(httpx.Client, "request", boom)
    monkeypatch.setattr(httpx.Client, "post", boom)
    assert server.slack_notify("c", "m", confirm=True)["dry_run"] is True
    assert server.sequencer_enqueue("1", "x")["dry_run"] is True


def test_live_path_uses_selected_http_adapter(monkeypatch):
    monkeypatch.setenv("SPEED_TO_LEAD_ADAPTERS", "notifier=slack")
    monkeypatch.setenv("ALLOW_LIVE_WRITES", "1")
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test")
    calls = []
    def post(self, url, **kw):
        calls.append(url)
        return httpx.Response(200, json=fixture("slack_ok.json"))
    monkeypatch.setattr(httpx.Client, "post", post)
    r = server.slack_notify("#revops", "hi", confirm=True)
    assert r["dry_run"] is False and r["adapter"] == "slack" and len(calls) == 1
