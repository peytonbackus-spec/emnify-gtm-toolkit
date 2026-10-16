---
id: contract-inbound-lead-qualifier
type: contract-index
tags: [contract, workflow-contract, inbound-sdr]
last_modified: 2026-09-25
---

# Inbound Lead Qualifier Agent -- Workflow Contract

Companion note for `inbound-lead-qualifier-contract.yaml` -- gives the YAML contract a markdown page so other notes can link to it with a real relative link instead of a bare filename.

**Real file:** `gtm-os/contracts/inbound-lead-qualifier-contract.yaml`

**Objective:** Enrich, dedupe, score, and route every new inbound lead within 5 minutes of CRM creation, before human review. **Role map:** `icp_fit_agent` (Tier 1/2/3 classification) -> `dedup_agent` (existing-record match check) -> `routing_agent` (territory assignment + Slack post). **Reads:** `wiki/skills/icp-builder`, `wiki/concepts/gtm-tool-data-models`. **Writes:** `intelligence/daily/`. **MCP tools:** `crm_read`, `crm_write_custom_fields_only`, `clay_enrich`, `slack_notify`. Promoted from the human-invoked [inbound-lead-qualifier](../agents/inbound-lead-qualifier.md) prompt agent.

## See Also
[inbound-lead-qualifier](../agents/inbound-lead-qualifier.md) . [00-Agent-Router](../agents/00-Agent-Router.md) . [full-org-agent-taxonomy](../../wiki/concepts/full-org-agent-taxonomy.md)
