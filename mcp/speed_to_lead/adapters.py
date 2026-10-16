"""Adapter interfaces and implementations for the speed-to-lead MCP server.

Interfaces: CRM.read_new_leads, Calendar.read_no_shows, Notifier.notify,
Sequencer.enqueue.  Implementations: mock (default), json (local file),
hubspot + slack (HTTP, UNVERIFIED -- never run against live accounts).

Write-side adapters (Notifier, Sequencer) are only invoked by server.py
after the dry-run / ALLOW_LIVE_WRITES / confirm gate has passed.
"""
from __future__ import annotations

import json
import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Optional

HERE = Path(__file__).resolve().parent


def data_dir() -> Path:
    return Path(os.environ.get("SPEED_TO_LEAD_DATA_DIR", HERE / "data"))


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


# ---------------------------------------------------------------- interfaces
class CRM(ABC):
    @abstractmethod
    def read_new_leads(self, since_minutes: int) -> list: ...


class Calendar(ABC):
    @abstractmethod
    def read_no_shows(self, lookback_hours: int) -> list: ...


class Notifier(ABC):
    @abstractmethod
    def notify(self, channel: str, message: str) -> dict: ...


class Sequencer(ABC):
    @abstractmethod
    def enqueue(self, contact_id: str, cadence_name: str) -> dict: ...


# ------------------------------------------------------- file-backed helpers
def _materialize(rec: dict, offset_key: str, ts_key: str) -> dict:
    """Turn `<offset_key>` (minutes ago) into an absolute ISO `<ts_key>`."""
    rec = dict(rec)
    if offset_key in rec:
        minutes = rec.pop(offset_key)
        rec[ts_key] = (now_utc() - timedelta(minutes=minutes)).isoformat()
    return rec


def _load(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def _leads_from(data: dict, since_minutes: int) -> list:
    cutoff = now_utc() - timedelta(minutes=since_minutes)
    leads = [_materialize(l, "created_minutes_ago", "created_at") for l in data.get("leads", [])]
    return [l for l in leads if parse_iso(l["created_at"]) >= cutoff]


def _no_shows_from(data: dict, lookback_hours: int) -> list:
    cutoff = now_utc() - timedelta(hours=lookback_hours)
    meetings = [_materialize(m, "scheduled_minutes_ago", "scheduled_at") for m in data.get("meetings", [])]
    return [
        m for m in meetings
        if m.get("status") == "no_show"
        and not m.get("recovery_triggered", False)
        and parse_iso(m["scheduled_at"]) >= cutoff
    ]


def _append_jsonl(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ----------------------------------------------------------------------- mock
class _FileData:
    filename = "mock_data.json"

    def __init__(self, path: Optional[Path] = None):
        self.path = Path(path) if path else data_dir() / self.filename

    def data(self) -> dict:
        return _load(self.path)


class MockCRM(_FileData, CRM):
    def read_new_leads(self, since_minutes):
        return _leads_from(self.data(), since_minutes)


class MockCalendar(_FileData, Calendar):
    def read_no_shows(self, lookback_hours):
        return _no_shows_from(self.data(), lookback_hours)


class MockNotifier(Notifier):
    log_name = "notification_log.jsonl"

    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = Path(log_path) if log_path else data_dir() / self.log_name

    def notify(self, channel, message):
        entry = {"channel": channel, "message": message, "sent_at": now_utc().isoformat()}
        _append_jsonl(self.log_path, entry)
        print(f"[MOCK notify] #{channel}: {message}", file=sys.stderr)
        return {"ok": True, "mock": True, **entry}


class MockSequencer(Sequencer):
    log_name = "notification_log.jsonl"

    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = Path(log_path) if log_path else data_dir() / self.log_name

    def enqueue(self, contact_id, cadence_name):
        entry = {"action": "sequencer_enqueue", "contact_id": contact_id,
                 "cadence_name": cadence_name, "enqueued_at": now_utc().isoformat()}
        _append_jsonl(self.log_path, entry)
        return {"ok": True, "mock": True, **entry}


# ----------------------------------------------------------------------- json
class JsonCRM(MockCRM):
    filename = "sample_leads.json"

    def __init__(self, path: Optional[Path] = None):
        env = os.environ.get("SPEED_TO_LEAD_JSON_PATH")
        super().__init__(path or (Path(env) if env else None))


class JsonCalendar(MockCalendar):
    filename = "sample_leads.json"

    def __init__(self, path: Optional[Path] = None):
        env = os.environ.get("SPEED_TO_LEAD_JSON_PATH")
        super().__init__(path or (Path(env) if env else None))


class JsonNotifier(MockNotifier):
    """Writes to a local outbox file; never touches the network."""
    log_name = "outbox.jsonl"

    def notify(self, channel, message):
        r = super().notify(channel, message)
        r.pop("mock", None)
        return {**r, "adapter": "json", "outbox": str(self.log_path)}


class JsonSequencer(MockSequencer):
    log_name = "outbox.jsonl"

    def enqueue(self, contact_id, cadence_name):
        r = super().enqueue(contact_id, cadence_name)
        r.pop("mock", None)
        return {**r, "adapter": "json", "outbox": str(self.log_path)}


# ------------------------------------------------------- HTTP (UNVERIFIED)
class AdapterError(RuntimeError):
    pass


def _http_client(client: Any = None):
    if client is not None:
        return client
    import httpx
    return httpx.Client(timeout=15.0)


class HubSpotBase:
    """UNVERIFIED: written from HubSpot's public API docs; never run against a
    real portal. Auth: private-app token in HUBSPOT_TOKEN (Bearer)."""
    BASE = "https://api.hubapi.com"

    def __init__(self, token: Optional[str] = None, client: Any = None):
        self.token = token or os.environ.get("HUBSPOT_TOKEN")
        self._client = client

    @property
    def http(self):
        if self._client is None:
            self._client = _http_client()
        return self._client

    def _req(self, method: str, path: str, **kw) -> dict:
        if not self.token:
            raise AdapterError("HUBSPOT_TOKEN is not set")
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        resp = self.http.request(method, self.BASE + path, headers=headers, **kw)
        if resp.status_code >= 400:
            raise AdapterError(f"HubSpot {method} {path} -> {resp.status_code}: {resp.text[:300]}")
        return resp.json() if resp.content else {}


class HubSpotCRM(HubSpotBase, CRM):
    """UNVERIFIED. POST /crm/v3/objects/contacts/search filtered on createdate.
    Tier comes from the contact property named by HUBSPOT_TIER_PROPERTY
    (default `score_tier`, expected values like "Tier 1 (Hot)")."""

    def read_new_leads(self, since_minutes):
        since_ms = int((now_utc() - timedelta(minutes=since_minutes)).timestamp() * 1000)
        tier_prop = os.environ.get("HUBSPOT_TIER_PROPERTY", "score_tier")
        body = {
            "filterGroups": [{"filters": [
                {"propertyName": "createdate", "operator": "GTE", "value": str(since_ms)}]}],
            "sorts": [{"propertyName": "createdate", "direction": "DESCENDING"}],
            "properties": ["firstname", "lastname", "email", "company", "createdate", tier_prop],
            "limit": 100,
        }
        data = self._req("POST", "/crm/v3/objects/contacts/search", json=body)
        out = []
        for r in data.get("results", []):
            p = r.get("properties", {})
            name = " ".join(x for x in (p.get("firstname"), p.get("lastname")) if x)
            out.append({
                "id": r["id"], "name": name, "email": p.get("email"),
                "company": p.get("company"),
                "score_tier": p.get(tier_prop) or "Tier 3 (Cold)",
                "created_at": p.get("createdate") or r.get("createdAt"),
            })
        return out


class HubSpotCalendar(HubSpotBase, Calendar):
    """UNVERIFIED. POST /crm/v3/objects/meetings/search for
    hs_meeting_outcome = NO_SHOW, then
    GET /crm/v4/objects/meetings/{id}/associations/contacts for the contact id.
    `recovery_triggered` is not a HubSpot field; meetings are treated as not yet
    recovered (dedupe on your side, e.g. via the sequence enrollment check)."""

    def read_no_shows(self, lookback_hours):
        since_ms = int((now_utc() - timedelta(hours=lookback_hours)).timestamp() * 1000)
        body = {
            "filterGroups": [{"filters": [
                {"propertyName": "hs_meeting_outcome", "operator": "EQ", "value": "NO_SHOW"},
                {"propertyName": "hs_meeting_start_time", "operator": "GTE", "value": str(since_ms)}]}],
            "properties": ["hs_meeting_title", "hs_meeting_start_time", "hs_meeting_outcome"],
            "limit": 100,
        }
        data = self._req("POST", "/crm/v3/objects/meetings/search", json=body)
        out = []
        for r in data.get("results", []):
            assoc = self._req("GET", f"/crm/v4/objects/meetings/{r['id']}/associations/contacts")
            ids = [a["toObjectId"] for a in assoc.get("results", [])]
            p = r.get("properties", {})
            out.append({
                "id": r["id"], "contact_id": str(ids[0]) if ids else None,
                "title": p.get("hs_meeting_title"),
                "scheduled_at": p.get("hs_meeting_start_time"),
                "status": "no_show", "recovery_triggered": False,
            })
        return out


class HubSpotSequencer(HubSpotBase, Sequencer):
    """UNVERIFIED. Needs HubSpot Sales/Service Hub Pro+ and scopes for sequences.
    Env: HUBSPOT_SEQUENCE_USER_ID, HUBSPOT_SENDER_EMAIL. `cadence_name` is looked up
    by name via GET /automation/v4/sequences, then
    POST /automation/v4/sequences/enrollments?userId=..."""

    def enqueue(self, contact_id, cadence_name):
        user_id = os.environ.get("HUBSPOT_SEQUENCE_USER_ID")
        sender = os.environ.get("HUBSPOT_SENDER_EMAIL")
        if not user_id or not sender:
            raise AdapterError("HUBSPOT_SEQUENCE_USER_ID and HUBSPOT_SENDER_EMAIL are required")
        seqs = self._req("GET", "/automation/v4/sequences", params={"userId": user_id, "limit": 100})
        match = [s for s in seqs.get("results", []) if s.get("name") == cadence_name]
        if not match:
            raise AdapterError(f"No HubSpot sequence named {cadence_name!r}")
        resp = self._req("POST", "/automation/v4/sequences/enrollments",
                         params={"userId": user_id},
                         json={"sequenceId": match[0]["id"], "contactId": str(contact_id),
                               "senderEmail": sender})
        return {"ok": True, "adapter": "hubspot", "contact_id": contact_id,
                "cadence_name": cadence_name, "enrollment": resp}


class SlackNotifier(Notifier):
    """UNVERIFIED. POST https://slack.com/api/chat.postMessage with a bot token in
    SLACK_BOT_TOKEN (scope chat:write). Slack replies HTTP 200 with ok=false on
    errors, which is surfaced as AdapterError."""
    URL = "https://slack.com/api/chat.postMessage"

    def __init__(self, token: Optional[str] = None, client: Any = None):
        self.token = token or os.environ.get("SLACK_BOT_TOKEN")
        self._client = client

    def notify(self, channel, message):
        if not self.token:
            raise AdapterError("SLACK_BOT_TOKEN is not set")
        if self._client is None:
            self._client = _http_client()
        resp = self._client.post(
            self.URL,
            headers={"Authorization": f"Bearer {self.token}",
                     "Content-Type": "application/json; charset=utf-8"},
            json={"channel": channel, "text": message})
        if resp.status_code >= 400:
            raise AdapterError(f"Slack HTTP {resp.status_code}: {resp.text[:300]}")
        body = resp.json()
        if not body.get("ok"):
            raise AdapterError(f"Slack error: {body.get('error', 'unknown')}")
        return {"ok": True, "adapter": "slack", "channel": body.get("channel", channel),
                "ts": body.get("ts"), "message": message}


# ------------------------------------------------------------------- registry
REGISTRY: dict = {
    "crm": {"mock": MockCRM, "json": JsonCRM, "hubspot": HubSpotCRM},
    "calendar": {"mock": MockCalendar, "json": JsonCalendar, "hubspot": HubSpotCalendar},
    "notifier": {"mock": MockNotifier, "json": JsonNotifier, "slack": SlackNotifier},
    "sequencer": {"mock": MockSequencer, "json": JsonSequencer, "hubspot": HubSpotSequencer},
}


def parse_selection(spec: Optional[str] = None) -> dict:
    """Parse 'crm=json,notifier=mock' -> full {kind: name} map (default mock)."""
    spec = os.environ.get("SPEED_TO_LEAD_ADAPTERS", "") if spec is None else spec
    sel = {k: "mock" for k in REGISTRY}
    for part in filter(None, (p.strip() for p in spec.split(","))):
        if "=" not in part:
            raise ValueError(f"Bad SPEED_TO_LEAD_ADAPTERS entry {part!r}; expected kind=name")
        kind, name = (x.strip().lower() for x in part.split("=", 1))
        if kind not in REGISTRY:
            raise ValueError(f"Unknown adapter kind {kind!r}; valid: {sorted(REGISTRY)}")
        if name not in REGISTRY[kind]:
            raise ValueError(f"Unknown {kind} adapter {name!r}; valid: {sorted(REGISTRY[kind])}")
        sel[kind] = name
    return sel


def get_adapter(kind: str, spec: Optional[str] = None):
    return REGISTRY[kind][parse_selection(spec)[kind]]()
