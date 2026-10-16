# speed-to-lead MCP server (adapter edition)

Five tools: `crm_read_new_leads`, `calendar_read_no_shows`, `evaluate_sla_breach`, `slack_notify`, `sequencer_enqueue`.

## Setup
1. Needs Python 3.10+ (the `mcp` SDK requires it): `uv venv --python 3.12 .venv` (or `python3.12 -m venv .venv`).
2. `uv pip install --python .venv/bin/python -r requirements.txt` (pins `mcp<2`; v2 renamed FastMCP). To reproduce the exact versions this server was last verified against, install with `pip install -r requirements.lock` instead.
3. `.venv/bin/python server.py --selftest` smoke-tests with mock data, no MCP client.
4. `.venv/bin/python -m pytest` runs the 27 tests (no network).
5. Pick backends: `SPEED_TO_LEAD_ADAPTERS="crm=json,calendar=json,notifier=mock,sequencer=mock"` (kinds: crm, calendar, notifier, sequencer; default all `mock`).
6. Options: crm/calendar = `mock|json|hubspot`; notifier = `mock|json|slack`; sequencer = `mock|json|hubspot`.
7. `json` reads `data/sample_leads.json` (override with `SPEED_TO_LEAD_JSON_PATH`); timestamps may be `created_minutes_ago` offsets so data never goes stale.
8. Writes (`slack_notify`, `sequencer_enqueue`) are DRY RUN unless env `ALLOW_LIVE_WRITES=1` AND the call passes `confirm=true`.
9. HubSpot/Slack env: `HUBSPOT_TOKEN`, `HUBSPOT_TIER_PROPERTY` (default `score_tier`), `HUBSPOT_SEQUENCE_USER_ID`, `HUBSPOT_SENDER_EMAIL`, `SLACK_BOT_TOKEN`.
10. Register with Claude Code (print only; run it yourself):

```
claude mcp add speed-to-lead --scope user -e SPEED_TO_LEAD_ADAPTERS="crm=json,calendar=json" -- ~/gtm-revops-toolkit/mcp/speed_to_lead/.venv/bin/python ~/gtm-revops-toolkit/mcp/speed_to_lead/server.py
```

## UNVERIFIED: HubSpot and Slack adapters
`HubSpotCRM`, `HubSpotCalendar`, `HubSpotSequencer` and `SlackNotifier` in `adapters.py` were written from public API docs and have only been tested against recorded fixtures with mocked HTTP. They have never touched a real HubSpot portal or Slack workspace. Endpoints, scopes (contacts, meetings, sequences; Slack `chat:write`), the sequences API availability (HubSpot Pro+ tiers), field names (`hs_meeting_outcome`, custom tier property) and response shapes need checking on a sandbox account before any live use. HubSpot has no `recovery_triggered` field, so no-show dedupe must be handled separately.

## Notes
- `evaluate_sla_breach` logic is unchanged from the original. Mock data now uses relative offsets (the original's absolute 2026-09-25 dates had expired).
- Mock/json notifier and sequencer write logs under `data/` (`notification_log.jsonl`, `outbox.jsonl`) only on live (gated) calls.
