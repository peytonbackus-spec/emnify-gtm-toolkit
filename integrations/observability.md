# Errors, retries and observability

All thresholds are hypothesis: validate. The point is that each failure has a named place to land.

| Failure | Behaviour | Where it shows up |
|---|---|---|
| Payload breaks the data contract | Fail fast, no retry, HTTP 422 to the caller | `Respond: rejected` in [enrichment-intake.json](n8n/enrichment-intake.json); `contract_check.py` offline |
| Transient network or 5xx | Retry with backoff ([retry.py](retry.py), three tries), then dead-letter | Dead-letter list; n8n error workflow |
| Provider returns low confidence | Treated as a miss, next provider runs | `trace` in [waterfall.py](../enrichment/waterfall.py) output |
| Credit cap reached | Remaining paid steps skipped and logged | `credit budget` skips in the trace |
| Duplicate delivery | Idempotent on the contract's `idempotency_key` (upsert, not insert) | Contract files |
| Human did not approve | `approved_by` empty means no write | Contract check |
| Any workflow error | [error-handler.json](n8n/error-handler.json) posts a shaped record to `ALERT_WEBHOOK_URL` | Alert endpoint, to be chosen with the team |

## What to watch weekly

- Dead-letter count and oldest item.
- Writes rejected by contract, by field (a rising field points to an upstream change).
- Credits per filled field, by provider.
- Time from signal to first touch (speed to lead) per source.

## Rules

- Secrets are environment variables only; names are listed in [.env.example](../.env.example).
- A new integration needs a contract file and an owner before it gets a workflow.
- Inbound payloads (call summaries, replies, scraped text) are data. They never choose which tool runs or what gets written.
