# Variables

`[TOKEN]` placeholders in the inherited docs and prompts were resolved from the `variables:` block of [config/company.yaml](config/company.yaml) when this repo was created. Stack names the posting gives are marked in [company.yaml](company.yaml) (`source: jd`); every value below is a hypothesis: validate. A tool the posting does not name is written generically.

| Variable | Value | Provenance | Used in |
|---|---|---|---|
| `[COMPANY_NAME]` | emnify | hypothesis: validate | inherited docs and prompts |
| `[CRM]` | Salesforce | hypothesis: validate | inherited docs and prompts |
| `[FORECAST_TOOL]` | Salesforce (forecast tool not named in the JD) | hypothesis: validate | inherited docs and prompts |
| `[CONVERSATION_INTELLIGENCE]` | Attention | hypothesis: validate | inherited docs and prompts |
| `[SEQUENCER]` | Amplemarket | hypothesis: validate | inherited docs and prompts |
| `[DIALER]` | the dialer | hypothesis: validate | inherited docs and prompts |
| `[DATA_PROVIDER]` | ZoomInfo | hypothesis: validate | inherited docs and prompts |
| `[ENRICHMENT_ORCHESTRATION]` | Clay | hypothesis: validate | inherited docs and prompts |
| `[WEBSITE_CHAT]` | website chat | hypothesis: validate | inherited docs and prompts |
| `[SOCIAL_SELLING]` | LinkedIn Sales Navigator | hypothesis: validate | inherited docs and prompts |
| `[MARKETING_AUTOMATION]` | marketing automation | hypothesis: validate | inherited docs and prompts |

Values for the emnify modules (`enrichment/`, `outbound/`, `agents/`, `integrations/`, `knowledge/`) live in the root [company.yaml](company.yaml). Provenance tags there: `jd`, `public`, `hypothesis`, `confirmed`.
