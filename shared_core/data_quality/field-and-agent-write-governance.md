# Field and Agent-Write Governance

Governance note for `shared_core/data_quality`. It sets who may create, change and delete CRM fields and records, including AI agents. [`dq_monitor.py`](dq_monitor.py) measures compliance, [CRM Health Scoring](../../docs/playbooks/CRM_Health_Scoring.md) trends it, and the [CRM cleanup contract](../../docs/contracts/crm-cleanup-contract.md) is the only path for agent corrections.

## 1. Data model follows the customer journey

Objects, properties and relationships map to lifecycle stages, not to the org chart or a tool. The connections that must exist:

- account to contacts;
- account to opportunities;
- contacts to opportunities (many-to-many through roles);
- opportunity to line items;
- account to subscriptions;
- activity to contact, account or opportunity.

A missing link is a reporting gap. Use a custom object only when there are many records per parent, history has to be kept separately, or an external system syncs it independently.

## 2. Field lifecycle

- **Create:** a request documents the name, purpose, owner, type and validation, source (manual, formula, integration or enrichment), the reports or automations it feeds, and a deprecation plan. Review checks for duplicates and whether a standard field would do. Decision within 5 business days, through the [CRM request intake](../../gtm_strategy_ops/sales_planning/crm-request-intake.md) queue (decision #21). The field is added to the data dictionary when it's created.
- **Naming:** functional prefixes (`rev_`, `mktg_`, `sales_`, `cs_`, `int_`, `calc_`). No `tmp_`, `test_` or `x_`.
- **Types:** picklists over free text for anything categorical; multi-select only when it's unavoidable; validation ranges on numbers.
- **Deprecate (practice-based timeline):**
  1. Announce it (2 weeks).
  2. Migrate the data and sample-check it (4 weeks).
  3. Hide it from views, forms and workflows but keep it readable (2 weeks, or 12 months for revenue, date and identifier fields).
  4. Export an archive, then delete after 6 months once no workflow, report or integration references it.
- **Rule:** a field with no documented owner and no documented use is a deprecation candidate.

## 3. System of record per data point

One system owns each data point and the others read it. Examples:
- account name: the CRM;
- firmographics: the enrichment vendor, synced to the CRM;
- stage: the CRM, with only Sales updating it;
- subscription dates: the finance system, read-only in the CRM.

Syncs are one-way by default. A bidirectional sync needs a per-field conflict rule and a 24-hour conflict SLA. Monitor syncs: alert after 3 failures, compare record counts weekly, alert on latency above 2 hours.

## 4. Enrichment write policy

| Data | Policy |
|---|---|
| Immutable facts (founding year, domain) | Auto-overwrite allowed |
| Data where manual entry is authoritative | Fill-if-empty only |
| Data that may conflict (size, title) | Suggest for review (default) |

Before engaging any enrichment vendor, get its DPA, data sources, transfer mechanism and SOC 2/ISO report. Prefer EU-based processing for EU data. CASL applies to Canadian contacts, and GDPR Art. 21 objections stop processing for direct marketing immediately.

## 5. Agent write guardrails

These extend [`hitl.py`](../ai_governance/hitl.py) and [earned autonomy](../ai_governance/earned-autonomy.md):

- **Protected fields:** agents never write to account name, created date or closed-won revenue.
- **Validation before any write** to a mutable field: is the value in range? Could it be a typo? Is an upstream failure behind it?
- **Holds on anomalies:** for example, ARR above a set limit on one deal is held for human review.
- **Merges:** agents surface candidates only; a human approves every merge.
- **Low confidence:** decisions on stage, writes or merges below about 65% confidence escalate to a human. An escalation rate above about 15% means the prompt or the upstream data is broken.
- **Audit trail:** every agent action logs what it read, what it decided, what it wrote, when, and its confidence, in an append-only log ([`outputs/ai_audit_log.jsonl`](../../outputs/ai_audit_log.jsonl) in this repo).
- **Prompts are versioned like code:** test against a sample before release, and notify the RevOps owner of any material change in behavior.

## 6. Definitions are governance too

Shared definitions (lead, MQL, pipeline, ARR, customer) are proposed by an owner, reviewed by Marketing, Sales and Finance, signed off by the revenue leader, published in [metric-definitions.md](../metrics/metric-definitions.md), and reviewed quarterly. Stage data requirements enforce them: a deal can't sit in a stage whose required fields are empty.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/rutger-katz/revops-data-governance` (MIT, © 2026 Swan). See the [crosswalk](../../docs/crosswalks/swan-gtm-skills.md)._
