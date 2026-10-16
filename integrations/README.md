# integrations/

The integration layer between Salesforce, Clay, ZoomInfo, Amplemarket, n8n, Attention, Weflow, Sales Navigator and Claude. Which of these are live at emnify is a hypothesis: validate.

| Piece | Status |
|---|---|
| [contracts/](contracts/) data contracts (YAML) and [contract_check.py](contract_check.py) | Real, offline |
| [n8n/enrichment-intake.json](n8n/enrichment-intake.json), [n8n/error-handler.json](n8n/error-handler.json) | Importable. Inactive. Dry-run unless `DRY_RUN=false` |
| [retry.py](retry.py) backoff + dead-letter | Real, offline |
| [clients.py](clients.py) Amplemarket, Attention, Weflow, Clay | Stubs. Raise without credentials, call nothing |
| [observability.md](observability.md) | Notes |

Who writes what (hypothesis: validate):

| System | Reads | Writes |
|---|---|---|
| Salesforce | everything below | system of record; only the n8n upsert and humans write |
| Clay | Salesforce account export | enriched rows, never Salesforce directly |
| n8n | Clay, Amplemarket | Salesforce (after approval), alerts |
| Amplemarket | approved lists | sequence activity |
| Attention, Weflow | n/a | call summaries and activity into Salesforce |
| Claude agents | [knowledge/](../knowledge/README.md) | proposals only |

Stack as configured in [company.yaml](../company.yaml):

<!-- BEGIN company:stack -->
| Need | Tool | Source | State |
|---|---|---|---|
| crm | Salesforce | jd | hypothesis: validate (system of record) |
| enrichment orchestration | Clay | jd | hypothesis: validate (must-have: walk through a flow) |
| data provider | ZoomInfo | jd | hypothesis: validate (licensed seats, credit model) |
| sequencer | Amplemarket | jd | hypothesis: validate (outbound engagement layer) |
| workflow automation | n8n | jd | hypothesis: validate (self-hosted vs cloud) |
| conversation intelligence | Attention | jd | hypothesis: validate (call data source) |
| salesforce sync | Weflow | jd | hypothesis: validate (activity and meeting capture into SFDC) |
| social selling | LinkedIn Sales Navigator | jd | hypothesis: validate |
| llm | Claude | jd | hypothesis: validate (API access and data-handling terms) |
<!-- END company:stack -->
