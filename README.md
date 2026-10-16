# emnify-gtm-toolkit

A working prototype of the outbound engine and enrichment infrastructure for the emnify GTM Engineer role. Private repo. Built from my GTM and RevOps toolkit template.

<!-- BEGIN company:role -->
emnify GTM Engineer (Senior (IC4), Sales Operations), reports to the Revenue Operations Lead, works with the CRO. Job 5004134101, posted 2026-10-13.
<!-- END company:role -->

**Everything about emnify in here is a hypothesis: validate.** I have no access to emnify's systems or data. Stack facts come from the posting, vertical facts from the public website, and every working assumption is labelled. Data in the repo is synthetic. Nothing calls an external service, and no credentials are present.

## What is here

| Folder | The posting's area | Real, offline | Stub or spec |
|---|---|---|---|
| [enrichment/](enrichment/README.md) | Lead enrichment end to end | Waterfall rules engine, dedupe, field-mapping contract | Salesforce and ZoomInfo clients, Clay table spec |
| [outbound/](outbound/README.md) | Pipeline coverage via outbound | Account scoring, consumption coverage model, handoff builder | Amplemarket push |
| [agents/](agents/README.md) | AI agents with Claude and Clay | Prompts, offline workflows, eval cases, review gate | Live model mode |
| [integrations/](integrations/README.md) | Integration layer | Data contracts, retry and dead-letter, importable n8n workflows | Amplemarket, Attention, Weflow, Clay clients |
| [knowledge/](knowledge/README.md) | Machine-readable company knowledge | Workflow contracts, validator, index, lookup | n/a |
| [ROADMAP.md](ROADMAP.md), [DECISIONS.md](DECISIONS.md), [ICP.md](ICP.md) | First six months, judgment, ICP | Documents | n/a |

Single source of values: [company.yaml](company.yaml). `python scripts/render_company_docs.py` regenerates the marked blocks in these docs from it.

## Stack named in the posting

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

## My results this is based on

From a previous role, mine and confirmed, not emnify's:

<!-- BEGIN company:proof -->
- Signal-based prospecting with Clay sourced about 80% of pipeline (Certa, confirmed)
- Deal-risk and pipeline-health scoring moved win rate from about 10% to about 15% (Certa, confirmed)
- Speed-to-lead went from 30 minutes to 5 minutes (Certa, confirmed)
- Security questionnaire and RFP turnaround went from 1.5-3 weeks to under 2 days, with human review kept (Certa, confirmed)
<!-- END company:proof -->

I have not claimed these for emnify and do not assume they transfer.

## Run it

```bash
pip install -r requirements.txt
python -m enrichment.run --dry-run
python -m outbound.run --dry-run
python -m agents.run_evals
python -m knowledge.tools validate
python -m pytest
```

## Inherited from the template

`shared_core/`, `gtm_engineer/` and `gtm_strategy_ops/` come from the template and run on synthetic data configured by [config/company.yaml](config/company.yaml), which holds generic example segments, not emnify's. See [docs/REPO_MAP.md](docs/REPO_MAP.md). `make data demo test` still works. Decision 7 in [DECISIONS.md](DECISIONS.md) explains why there are two config files.

## Not here, on purpose

- No live runs in Clay, Salesforce, ZoomInfo, Amplemarket, Attention or Weflow.
- No emnify data, contacts or internal information.
- No performance claims for the models in this repo. The coverage and scoring numbers are placeholders that show arithmetic.
