# enrichment/

Lead and account enrichment end to end: dedupe, waterfall, field-mapping contract, Salesforce upsert.

| File | What it is | Real or stub |
|---|---|---|
| [waterfall_rules.yaml](waterfall_rules.yaml) | Provider order, conditions, costs per field | Real (orderings are hypothesis: validate) |
| [waterfall.py](waterfall.py) | Rules engine: structured conditions (no `eval`), credit budget, full trace | Real, offline |
| [dedupe.py](dedupe.py) | Domain and name+country clustering, outputs a merge plan | Real, offline |
| [field_mapping.yaml](field_mapping.yaml) + [mapping.py](mapping.py) | Contract from enrichment output to Salesforce, with write policies | Real; SFDC API names are placeholders |
| [sfdc_client.py](sfdc_client.py) | Salesforce upsert | Stub (dry-run works) |
| [zoominfo_client.py](zoominfo_client.py) | ZoomInfo provider | Stub |
| [clay_table_spec.md](clay_table_spec.md) | The Clay flow, column by column | Spec only, no live run |
| [fixtures/](fixtures/provider_fixtures.json) | Synthetic provider responses | Synthetic |

```bash
python -m enrichment.run --dry-run
```

The older [gtm_engineer/enrichment/](../gtm_engineer/enrichment/) engines come from the template. This folder is the emnify-specific layer; its waterfall conditions are structured data, not evaluated strings.
