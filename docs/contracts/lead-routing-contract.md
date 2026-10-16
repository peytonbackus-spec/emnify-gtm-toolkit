---
id: contract-lead-routing
type: contract-index
tags: [contract, workflow-contract, lead-routing, inbound]
last_modified: 2026-10-13
---

# Lead Routing Agent -- Workflow Contract

Companion note for [`lead-routing-contract.yaml`](lead-routing-contract.yaml). This gives the YAML contract a markdown page that other notes can link to.

**Objective:** give every inbound lead exactly one owner, or a nurture or no-outreach queue, through an ordered rule list. The reason is stamped on the record, and first-touch SLAs are enforced by tier. It is a router, not a sender.

**Role map:**
1. `objection_gate_agent`: GDPR Art. 21, unsubscribe and CASL consent come first.
2. `account_match_agent`: existing opportunity, customer or churned account.
3. `fit_gate_agent`: MQL threshold.
4. `assignment_agent`: territory, then weighted round-robin with availability checks.
5. `sla_timer_agent`: hands off to the [speed-to-lead SLA contract](speed-to-lead-sla-contract.md).

**Reads:** `route_leads.py`, the Salesforce routing flow spec and config. **Writes:** `outputs/routed_leads.csv` and a routing review queue. **MCP tools:** `crm_read`, `crm_update_owner` (owner and reason fields only), `slack_notify`.

**How it maps to the existing engine:** [`route_leads.py`](../../gtm_engineer/lead_routing/route_leads.py) already implements rules R1-R7. This contract adds what the engine lacks:
- the objection/consent step 0, ahead of R1;
- churned-account and unowned-account handling inside R2/R3;
- availability skips in R6;
- the quarterly routing audit in the YAML.

**HITL:** `route_to_ae` is already on the always-review list in [`hitl.py`](../../shared_core/ai_governance/hitl.py). Any AI-assisted assignment stays in review until its override log supports promotion under [earned autonomy](../../shared_core/ai_governance/earned-autonomy.md), and never past decision #6.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/rutger-katz/lead-routing` (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._

## See Also
[speed-to-lead-sla-contract](speed-to-lead-sla-contract.md) . [casl-compliance-gate-contract](casl-compliance-gate-contract.md) . [salesforce-routing-flow-spec](../../gtm_engineer/lead_routing/salesforce-routing-flow-spec.md)
