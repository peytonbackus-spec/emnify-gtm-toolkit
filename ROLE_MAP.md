# Role map: the posting, side by side

Each row is something the posting says the role owns or screens for, and the file that answers it. Legend: ▶️ runs offline, 📐 spec or stub. Everything about emnify is hypothesis: validate.

<!-- BEGIN company:role -->
emnify GTM Engineer (Senior (IC4), Sales Operations), reports to the Revenue Operations Lead, works with the CRO. Job 5004134101, posted 2026-10-13.
<!-- END company:role -->

| Posting says | Answered by | Status |
|---|---|---|
| Owns the outbound engine and data enrichment infrastructure | [`enrichment/`](enrichment/README.md), [`outbound/`](outbound/README.md) | ▶️ |
| Lead enrichment end to end (Clay, ZoomInfo, first and second party data into Salesforce) | [waterfall](enrichment/waterfall.py), [dedupe](enrichment/dedupe.py), [mapping contract](enrichment/field_mapping.yaml) | ▶️ |
| Clay is a must-have: walk through a flow | [Clay table spec](enrichment/clay_table_spec.md), [walkthrough](docs/WALKTHROUGH.md) | 📐 no live run |
| ZoomInfo | [provider stub](enrichment/zoominfo_client.py) | 📐 |
| Salesforce | [upsert stub](enrichment/sfdc_client.py), [contract](integrations/contracts/salesforce_account_upsert.yaml) | 📐 |
| Pipeline coverage through outbound workflows | [scoring](outbound/scoring.py), [coverage](outbound/coverage.py), [sensitivity](outbound/sensitivity.py) | ▶️ |
| Amplemarket | [handoff builder](outbound/handoff.py), [spec](outbound/amplemarket_handoff.md) | ▶️ builder, 📐 push |
| Consumption-based revenue makes forecasting hard | [coverage in realized-usage terms](outbound/coverage.py), [metric definitions](knowledge/definitions/revenue-metrics.yaml), [qualification contract](knowledge/process/consumption-qualification.yaml) | ▶️ |
| AI agents with Claude | [`agents/`](agents/README.md): prompts, workflows, evals, review gate | ▶️ mock mode |
| n8n | [workflow JSON](integrations/n8n/enrichment-intake.json), [error handler](integrations/n8n/error-handler.json) | ▶️ importable, inactive |
| Attention, Weflow, Sales Navigator | [contracts](integrations/contracts/) and [stubs](integrations/clients.py) | 📐 |
| Integration layer observability | [`observability.md`](integrations/observability.md), [retry](integrations/retry.py) | ▶️ |
| Machine-readable company knowledge for agents | [`knowledge/`](knowledge/README.md) | ▶️ |
| Ships before the plan is perfect | [week 3-4 first run](ROADMAP.md) | plan |
| Measured on revenue outcomes, not tickets | [definitions](knowledge/definitions/revenue-metrics.yaml), [DECISIONS](DECISIONS.md) | doc |
| Pushes back respectfully on wrong solutions | [push-back examples](DECISIONS.md) | doc |
| First six months | [ROADMAP](ROADMAP.md) | doc |
| Functional assessment (case study or presentation) | [walkthrough](docs/WALKTHROUGH.md), [sample runs](docs/examples/emnify-sample-runs.md) | prep |
