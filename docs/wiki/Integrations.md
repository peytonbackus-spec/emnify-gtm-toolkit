# Integrations

Folder: `integrations/`.

- **Data contracts** (YAML): Salesforce account upsert, Amplemarket handoff, Attention call summary, Weflow activity, Sales Navigator signal. Each names an idempotency key. A checker validates payloads offline.
- **n8n workflows**: an enrichment intake (webhook, contract check, dry-run branch, live path unreachable unless `DRY_RUN=false`) and an error handler. Both import inactive.
- **Retry**: exponential backoff for transient errors only; contract errors fail fast; exhausted retries go to a dead-letter list.
- **Client stubs**: Amplemarket, Attention, Weflow, Clay. They raise without credentials and call nothing.

Failure paths and the weekly watch list are in `observability.md`. Which of these tools are live at emnify is a hypothesis: validate.
