# Variables

`[TOKEN]` placeholders in docs and prompts resolve from the `variables:` block of the config when a new repo is scaffolded (`make new`). In this template they hold neutral example values.

| Variable | Example value | Meaning |
|---|---|---|
| `[COMPANY_NAME]` | Example Co | Company name |
| `[CRM]` | Salesforce | System of record |
| `[FORECAST_TOOL]` | Clari | Forecasting platform |
| `[CONVERSATION_INTELLIGENCE]` | Gong | Call recording and analysis |
| `[SEQUENCER]` | Outreach | Sales engagement |
| `[DIALER]` | Orum | Dialer |
| `[DATA_PROVIDER]` | Apollo | Contact and company data |
| `[ENRICHMENT_ORCHESTRATION]` | Clay | Enrichment workflow tool |
| `[WEBSITE_CHAT]` | Drift | Conversational marketing |
| `[SOCIAL_SELLING]` | LinkedIn Sales Navigator | Social selling tool |
| `[MARKETING_AUTOMATION]` | HubSpot | Marketing automation (forms, email, subscription status) |

Add a variable by putting it under `variables:` in `config/example.yaml`, then use `[NAME]` in any `.md`/`.py` file. Tags `[ASSUME]`, `[PUBLIC]`, `[POSTING]`, `[VERIFY]` are provenance labels, not variables.
